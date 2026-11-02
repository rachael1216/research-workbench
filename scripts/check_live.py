#!/usr/bin/env python3
"""Small read-only public endpoint probes; reports failures honestly."""
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'plugins/research-workbench'))
from research_mcp import core


async def main():
    results = []
    for source, query in [('crossref', 'drift diffusion model'), ('pubmed', 'reinforcement learning cognition'), ('arxiv', 'all:predictive AND all:coding')]:
        try:
            data = await core.search(query, source, limit=2)
            result = {k: data[k] for k in ('source', 'query', 'searched_at_utc', 'request_url', 'total', 'returned')}
            result['status'] = 'ok'
            result['sample'] = data['records'][0] if data['records'] else None
        except Exception as exc:
            result = {'source': source, 'query': query, 'status': 'error', 'error': str(exc)}
        results.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    try:
        data = await core.doi_metadata('10.1038/nature14539')
        result = {'tool': 'verify_doi', 'status': 'ok', 'record': data['record'], 'checked_at_utc': data['checked_at_utc']}
    except Exception as exc:
        result = {'tool': 'verify_doi', 'status': 'error', 'error': str(exc)}
    results.append(result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    target = Path(__file__).resolve().parents[1] / 'docs/live-check.json'
    target.write_text(json.dumps({'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'results': results}, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    asyncio.run(main())
