import {test} from 'node:test';
import assert from 'node:assert/strict';
import {renderToStaticMarkup} from 'react-dom/server';
import {renderMarkdown} from '../src/theme/DocItem/Content/markdown.mjs';

test('tool descriptions render CommonMark and keep raw HTML inert', () => {
  const html = renderToStaticMarkup(renderMarkdown('Use ``source`` and *emphasis*.\n\n[link](https://example.com)\n\n<script>alert(1)</script>'));
  assert.match(html, /<code>source<\/code>/);
  assert.match(html, /<em>emphasis<\/em>/);
  assert.match(html, /<a href="https:\/\/example.com">link<\/a>/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.equal((html.match(/<p>/g) || []).length, 2);
});

test('tool descriptions do not create unsafe links', () => {
  const html = renderToStaticMarkup(renderMarkdown('[bad](javascript:alert%281%29)'));
  assert.doesNotMatch(html, /href=/);
});
