#!/usr/bin/env python3
"""Real stdio handshake, discovery and tool calls against the configured server command."""
import asyncio
import argparse
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def smoke(plugin: Path):
    params = StdioServerParameters(command='uv', args=['run', '--frozen', '--project', str(plugin), 'python', '-m', 'research_mcp.server'], cwd=str(plugin))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = await session.list_tools()
            names = {t.name for t in listed.tools}
            expected = {'get_research_guide', 'search_literature', 'verify_doi', 'audit_prose', 'compare_protected_content', 'environment_report'}
            assert names == expected, names
            calls = [('get_research_guide', {'stage': 'theory'}), ('audit_prose', {'text': '值得注意的是，进行了分析。'}),
                     ('compare_protected_content', {'before': 'n=12', 'after': 'n=13'}), ('environment_report', {})]
            for name, arguments in calls:
                result = await session.call_tool(name, arguments)
                assert not result.isError, (name, result)
                assert result.content, name
            invalid = await session.call_tool('get_research_guide', {'stage': '../../.env'})
            assert invalid.isError, 'Invalid guide must report an error'
            print('PASS: stdio initialize, 6 tools discovered, 4 calls and error handling')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plugin', type=Path, default=Path(__file__).resolve().parents[1] / 'plugins/research-workbench')
    args = parser.parse_args()
    asyncio.run(smoke(args.plugin.resolve()))
