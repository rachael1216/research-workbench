import asyncio
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'plugins/research-workbench'))
from research_mcp import core


class CoreTests(unittest.TestCase):
    def test_guides_are_contained(self):
        for stage in core.STAGES:
            self.assertTrue(core.guide(stage))
        with self.assertRaises(ValueError):
            core.guide('../../.env')

    def test_doi_normalization(self):
        self.assertEqual(core.normalize_doi('https://doi.org/10.1234/AB'), '10.1234/AB')
        with self.assertRaises(ValueError):
            core.normalize_doi('https://localhost/private')

    def test_protected_changes(self):
        source = r'Accuracy 91.2% \cite{smith2024}; $x^2$ [3] https://example.org/a'
        self.assertTrue(core.compare_content(source, source)['unchanged_for_checked_patterns'])
        altered = source.replace('91.2%', '95.2%').replace('x^2', 'x^3').replace('smith2024', 'other')
        changes = core.compare_content(source, altered)['changes']
        self.assertIn('numbers', changes)
        self.assertIn('math', changes)
        self.assertIn('latex_citations', changes)
        duplicated = core.compare_content('n=12; n=12', 'n=12')
        self.assertFalse(duplicated['unchanged_for_checked_patterns'])

    def test_prose_cues_are_not_verdicts(self):
        result = core.prose_audit('值得注意的是，我们进行数据分析。 Moreover, evaluation of X is useful.')
        kinds = {x['kind'] for x in result['findings']}
        self.assertIn('filler', kinds)
        self.assertIn('nominalization-cue', kinds)
        self.assertNotIn('score', result)

    def test_environment_report(self):
        result = core.environment()
        self.assertTrue(result['executable'])
        self.assertIn('mcp', result['packages'])


class NetworkContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_crossref_provenance_and_no_fake_claim_support(self):
        async def fake(url, params=None):
            self.assertEqual(params['rows'], 2)
            return httpx.Response(200, request=httpx.Request('GET', url, params=params), json={'message': {
                'total-results': 12, 'items': [{'title': ['A study'], 'DOI': '10.1234/a', 'published': {'date-parts': [[2024]]}}]}})
        with patch.object(core, 'request', fake):
            result = await core.search('a study', limit=2)
        self.assertEqual(result['returned'], 1)
        self.assertEqual(result['total'], 12)
        self.assertIn('searched_at_utc', result)
        self.assertEqual(result['records'][0]['access_level'], 'metadata')

    async def test_provider_failure_is_error_not_empty_search(self):
        async def fail(url, params=None):
            request = httpx.Request('GET', url)
            raise httpx.HTTPStatusError('rate limited', request=request, response=httpx.Response(429, request=request))
        with patch.object(core, 'request', fail):
            with self.assertRaises(httpx.HTTPStatusError):
                await core.search('learning')

    async def test_arxiv_abstract_extraction(self):
        xml = '''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:op="http://a9.com/-/spec/opensearch/1.1/"><op:totalResults>1</op:totalResults><entry><id>http://arxiv.org/abs/1234.5678v1</id><title>A model</title><author><name>A Person</name></author><summary>Example abstract.</summary><published>2024-01-01</published></entry></feed>'''
        async def fake(url, params=None):
            return httpx.Response(200, request=httpx.Request('GET', url), text=xml)
        with patch.object(core, 'request', fake):
            result = await core.search('all:model', 'arxiv')
        self.assertEqual(result['records'][0]['access_level'], 'abstract')
        self.assertEqual(result['total'], 1)

    async def test_pubmed_query_error_is_not_zero_results(self):
        async def fake(url, params=None):
            return httpx.Response(200, request=httpx.Request('GET', url), json={'esearchresult': {'count': '0', 'errorlist': {'fieldnotfound': ['oops']}}})
        with patch.object(core, 'request', fake):
            with self.assertRaises(ValueError):
                await core.search('x[oops]', 'pubmed')

    async def test_invalid_arguments_never_make_network_call(self):
        for kwargs in ({'query': ''}, {'query': 'x', 'source': 'file'}, {'query': 'x', 'limit': 100}):
            with self.assertRaises(ValueError):
                await core.search(**kwargs)


if __name__ == '__main__':
    unittest.main()
