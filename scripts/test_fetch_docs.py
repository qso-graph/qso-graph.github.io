import unittest
import json
import tempfile
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from scripts import fetch_docs
from scripts.fetch_docs import product_path, product_text, sanitize_html, take_title


class ManifestTests(unittest.TestCase):
    def test_fetch_records_repository_description_and_release(self):
        repo = {'name': 'example', 'private': False, 'archived': False,
                'topics': ['qso-graph-tool'], 'description': 'A useful tool'}
        release = {'draft': False, 'prerelease': False, 'tag_name': 'v1.2.3'}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs.lock').write_text('{}')
            with patch.object(fetch_docs, 'ROOT', root), \
                 patch.object(fetch_docs, 'pages', side_effect=[[repo], [release]]), \
                 patch.object(fetch_docs, 'product_files', return_value={'README.md': b'# Example\n'}):
                fetch_docs.main()
            manifest = json.loads((root / 'data' / 'docs.json').read_text())
        self.assertEqual(manifest[0]['description'], 'A useful tool')
        self.assertEqual(manifest[0]['tag'], 'v1.2.3')
        self.assertEqual(manifest[0]['section'], 'tools')
        self.assertEqual(manifest[0]['sections'], ['tools'])

    def test_multiple_sections_use_first_as_home(self):
        self.assert_sections(['qso-graph-library', 'qso-graph-app'],
                             ['applications', 'libraries'])

    def test_infra_with_section_is_a_product(self):
        self.assert_sections(['qso-graph-infra', 'qso-graph-library'], ['libraries'])

    def assert_sections(self, topics, expected):
        repo = {'name': 'example', 'private': False, 'archived': False, 'topics': topics}
        release = {'draft': False, 'prerelease': False, 'tag_name': 'v1.2.3'}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs.lock').write_text('{}')
            with patch.object(fetch_docs, 'ROOT', root), \
                 patch.object(fetch_docs, 'pages', side_effect=[[repo], [release]]), \
                 patch.object(fetch_docs, 'product_files', return_value={'README.md': b'# Example\n'}):
                fetch_docs.main()
            manifest = json.loads((root / 'data' / 'docs.json').read_text())
            self.assertEqual(manifest[0]['sections'], expected)
            self.assertEqual(manifest[0]['section'], expected[0])
            for section in expected:
                self.assertEqual((root / 'src/content/docs' / section / 'example/index.md').exists(),
                                 section == expected[0])

    def test_repositories_without_section_are_logged_and_skipped(self):
        repos = [{'name': name, 'private': False, 'archived': False, 'topics': topics}
                 for name, topics in [('plain', []), ('infra', ['qso-graph-infra'])]]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs.lock').write_text('{}')
            output = io.StringIO()
            with patch.object(fetch_docs, 'ROOT', root), \
                 patch.object(fetch_docs, 'pages', return_value=repos), redirect_stdout(output):
                fetch_docs.main()
            self.assertEqual(json.loads((root / 'data/docs.json').read_text()), [])
            self.assertIn('plain: no section topic; skipped', output.getvalue())
            self.assertIn('infra: infrastructure; skipped', output.getvalue())


class SanitizerTests(unittest.TestCase):
    def test_removes_active_elements_and_their_contents(self):
        text = '<p>safe<script>alert(1)</script><style>x</style><iframe>bad</iframe><object>bad</object><embed src="x">ok</p>'
        self.assertEqual(sanitize_html(text), '<p>safeok</p>')

    def test_removes_event_handlers_and_obfuscated_javascript_urls(self):
        text = '<a ONclick="bad()" href="&#x6a;ava&#x73;cript:alert(1)" title="ok">link</a><img src="javascript:bad" onerror=bad alt="safe">'
        self.assertEqual(sanitize_html(text), '<a title="ok">link</a><img alt="safe">')

    def test_preserves_markdown_and_safe_html(self):
        text = '# Title\n\n[link](https://example.org)\n\n<p><img src="https://example.org/a.png" alt="A &amp; B"></p>\n'
        self.assertEqual(sanitize_html(text), text)

    def test_preserves_urls_entities_and_tag_spelling(self):
        text = ("[link](https://example.org/?a=1&color=blue&b=2)\n"
                "![image](https://example.org/i.png?a=1&color=blue&b=2)\n"
                "&amp; &copy; &#169; bare & text\n"
                "<DIV  title='A &amp; B' data-x = unquoted >x</DIV>")
        self.assertEqual(sanitize_html(text), text)

    def test_preserves_autolinks_and_removes_markdown_javascript_links(self):
        self.assertEqual(sanitize_html('<https://example.org> <me@example.org>'), '<https://example.org> <me@example.org>')
        self.assertEqual(sanitize_html('[bad](javascript:alert)'), '[bad](#)')
        self.assertEqual(sanitize_html('<a href="java&#x09;script:alert">x</a>'), '<a>x</a>')

    def test_preserves_placeholders_in_code_and_prose(self):
        placeholders = '<version> <fingerprint> <NAME>'
        text = (f'Inline `{placeholders}` and prose {placeholders}.\n\n'
                f'```text\n{placeholders}\n<script>alert(1)</script>\n```\n'
                '<script>alert(1)</script>')
        expected = (f'Inline `{placeholders}` and prose '
                    f'{placeholders}.\n\n'
                    f'```text\n{placeholders}\n<script>alert(1)</script>\n```\n')
        self.assertEqual(sanitize_html(text), expected)

    def test_preserves_code_with_active_looking_content(self):
        text = '`<script>alert(1)</script> [x](javascript:bad)`\n~~~\n<a onclick="x">\n~~~\n'
        self.assertEqual(sanitize_html(text), text)

    def test_preserves_non_active_attributes(self):
        self.assertEqual(sanitize_html('<div class="example" data-id="1">text</div>'),
                         '<div class="example" data-id="1">text</div>')

    def test_preserves_file_types(self):
        self.assertEqual(product_path('README.md'), 'index.md')
        self.assertEqual(product_path('docs/user/guide.md'), 'guide.md')
        self.assertEqual(product_path('docs/user/guide.mdoc'), 'guide.mdoc')
        self.assertEqual(product_path('docs/user/sub/README.md'), 'sub/index.md')


if __name__ == '__main__':
    unittest.main()


class TitleTests(unittest.TestCase):
    """Starlight prints the title as the page heading, so a README's own first heading moves there."""

    def test_first_heading_becomes_the_title_and_leaves_the_body(self):
        page = product_text('README.md', b'<!-- mcp-name: x -->\n# pota-mcp\n\nText.\n\n## Install\n', {}, 'pota-mcp', 'v1.0.0')
        self.assertTrue(page.startswith('---\ntitle: "pota-mcp"\n---\n'))
        self.assertNotIn('# pota-mcp', page)
        self.assertIn('## Install', page)
        self.assertIn('<!-- mcp-name: x -->', page)

    def test_a_hash_line_in_a_fence_is_code_not_a_title(self):
        title, body = take_title('```sh\n# install it\nuvx pota-mcp\n```\n\n# Real title\n')
        self.assertEqual(title, 'Real title')
        self.assertIn('# install it', body)
        self.assertNotIn('# Real title', body)

    def test_no_heading_keeps_the_body(self):
        self.assertEqual(take_title('Just text.\n'), (None, 'Just text.\n'))
