"""Build the product navigation and retain legacy server links."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABELS = {'applications': 'Applications', 'mcp-servers': 'MCP Servers',
          'libraries': 'Libraries', 'tools': 'Tools'}



def manifest():
    path = ROOT / 'data/docs.json'
    return json.loads(path.read_text()) if path.exists() else []


def on_config(config):
    products = manifest()
    nav = [{'Home': 'index.md'}, {'Products': 'products.md'}, {'Specification': 'specification.md'}]
    for section, title in LABELS.items():
        entries = []
        for product in sorted((p for p in products if p['section'] == section), key=lambda p: p['repo']):
            base = Path(section) / product['repo']
            pages = sorted((ROOT / 'docs' / base).rglob('*.md'))
            index = (base / 'index.md').as_posix()
            children = [index]
            children.extend({p.stem.replace('-', ' ').replace('_', ' ').title(): p.relative_to(ROOT / 'docs').as_posix()}
                            for p in pages if p.relative_to(ROOT / 'docs').as_posix() != index)
            entries.append({product['repo']: children})
        if section == 'mcp-servers':
            entries = ['servers/index.md', {'Getting Started': 'getting-started.md'},
                       {'Credential Setup': 'credentials.md'}] + entries
        nav.append({title: entries})
    nav += [{'Architecture': 'architecture.md'}, {'Testing': 'testing.md'}, {'Security': 'security.md'},
            {'About': ['about/index.md', {'Attributions': 'about/attributions.md'},
                       {'Contributing': 'about/contributing.md'}]}]
    config.nav = nav
    return config


def on_page_markdown(markdown, page, config, files):
    src = page.file.src_uri
    if src == 'products.md':
        links = ['- [' + p['repo'] + '](' + p['section'] + '/' + p['repo'] + '/index.md)' for p in sorted(manifest(), key=lambda p: p['repo'])]
        markdown += '\n\n## Released product documentation\n\n' + '\n'.join(links) + '\n'
    if src.startswith('mcp-servers/') and src.endswith('/index.md'):
        repo = src.split('/')[1]
        data = ROOT / 'data/servers.json'
        if not data.exists():
            raise RuntimeError('Missing server data; run scripts/collect_servers.py')
        if data.exists():
            servers = json.loads(data.read_text())
            product = next((p for p in manifest() if p['repo'] == repo), None)
            server = next((s for s in servers.values() if s['repo'] == repo), None)
            if not server or not product or product['tag'] != 'v' + server['version']:
                raise RuntimeError(f'{repo}: missing matching released package data')
            if server['kind'] == 'server':
                import importlib.util
                spec = importlib.util.spec_from_file_location('site_macros', ROOT / 'main.py')
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                _tool_reference = module._tool_reference
                markdown += '\n\n---\n\n' + _tool_reference(server['tool_details'])
    return markdown
