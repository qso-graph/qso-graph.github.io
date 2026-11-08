import {fromMarkdown} from 'mdast-util-from-markdown';
import {toHast} from 'mdast-util-to-hast';
import {toJsxRuntime} from 'hast-util-to-jsx-runtime';
import {Fragment, jsx, jsxs} from 'react/jsx-runtime';

// Raw HTML is displayed literally, never interpreted as markup.
function escapeHtmlNodes(node) {
  if (node.type === 'html') node.type = 'text';
  for (const child of node.children || []) escapeHtmlNodes(child);
}

function safeUrls(node) {
  for (const key of ['href', 'src']) {
    const value = node.properties?.[key];
    const normalized = typeof value === 'string' ? value.replace(/[\u0000-\u0020]/g, '') : '';
    if (/^[a-z][a-z\d+.-]*:/i.test(normalized) &&
        !/^(https?:|mailto:)/i.test(normalized)) {
      delete node.properties[key];
    }
  }
  for (const child of node.children || []) safeUrls(child);
}

export function renderMarkdown(text) {
  const tree = fromMarkdown(text);
  escapeHtmlNodes(tree);
  const html = toHast(tree);
  safeUrls(html);
  return toJsxRuntime(html, {Fragment, jsx, jsxs});
}
