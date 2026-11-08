import path from 'node:path';
import {readFileSync} from 'node:fs';
const products = JSON.parse(readFileSync('./data/docs.json'));
export default function productLinks() {
 return (tree, file) => {
  const filename = file.path.replaceAll('\\', '/');
  const product = products.find(p => filename.includes(`/docs/${p.section}/${p.repo}/`));
  if (!product) return;
  const rel = filename.split(`/docs/${product.section}/${product.repo}/`)[1];
  const origin = path.posix.dirname(product.sources[rel]);
  const rewrite = (url, image) => {
   if (/^(?:[a-z][a-z\d+.-]*:|\/|#|\/\/)/i.test(url)) return url;
   const [pathname, suffix = ''] = url.split(/(?=[?#])/, 2);
   const resolved = path.posix.normalize(path.posix.join(origin, pathname));
   const local = Object.entries(product.sources).find(([,source]) => source.toLowerCase() === resolved.toLowerCase());
   if (local) return `/${product.section}/${product.repo}/${local[0].replace(/(?:^|\/)index\.md(?:oc)?$/i, '').replace(/\.md(?:oc)?$/i, '/')}${suffix}`;
   if (resolved.startsWith('docs/user/') && !/\.md(?:oc)?$/i.test(resolved)) return `/${product.section}/${product.repo}/${resolved.slice(10)}${suffix}`;
   return `https://github.com/qso-graph/${product.repo}/${image ? 'raw' : 'blob'}/${product.tag}/${resolved}${suffix}`;
  };
  const visit = node => {if ((node.type === 'link' || node.type === 'image' || node.type === 'definition') && node.url) node.url = rewrite(node.url,node.type === 'image'); if (node.type === 'html' && node.value) node.value = node.value.replace(/\b(href|src)=(["'])([^"']+)\2/g, (_, attr, quote, url) => `${attr}=${quote}${rewrite(url, attr === 'src')}${quote}`); if (node.children) node.children.forEach(visit);};
  visit(tree);
 };
}
