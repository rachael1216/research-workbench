#!/usr/bin/env python3
"""Validate manifests and linked skill references without external services."""
import json
from pathlib import Path
import re
import yaml

root = Path(__file__).resolve().parents[1]
p = root / 'plugins/research-workbench'
portable = json.loads((p / 'plugin.json').read_text())
legacy = json.loads((p / '.codex-plugin/plugin.json').read_text())
assert portable['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
for key in ('name', 'version', 'description', 'license'):
    assert portable[key] == legacy[key], key
assert portable['extensions']['com.openai']['interface'] == legacy['interface']
assert len(legacy['interface']['shortDescription']) <= 30
servers = json.loads((p / 'mcp.json').read_text())['mcpServers']
compat = json.loads((p / '.mcp.json').read_text())['mcpServers']
for name, server in servers.items():
    assert server['type'] == 'stdio'
    assert {k:v for k,v in server.items() if k != 'type'} == compat[name]
for skill in (p / 'skills').glob('*/SKILL.md'):
    text = skill.read_text()
    front = yaml.safe_load(text.split('---', 2)[1])
    assert front['name'] == skill.parent.name
    assert isinstance(front['description'], str) and front['description']
    for link in re.findall(r'\]\(([^)]+\.md)\)', text):
        assert (skill.parent / link).is_file(), link
for item in json.loads((root / 'docs/sources.json').read_text()):
    assert re.fullmatch(r'[0-9a-f]{40}', item['blob_sha'])
assert not any(p.rglob('.env'))
print('PASS: portable/compat manifests, skill links, source IDs')
