import { readFile, writeFile, readdir, mkdir, copyFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve links at build time without changing the fetched README text.
export default function productLinks() {
  return { name: 'product-links', hooks: { 'astro:build:done': async ({ dir }) => {
    const root = process.cwd();
    const output = fileURLToPath(dir);
    const products = JSON.parse(await readFile(path.join(root, 'data/docs.json'), 'utf8'));
    for (const product of products) {
      const source = path.join(root, 'src/content/docs', product.section, product.repo);
      const destination = path.join(output, product.section, product.repo);
      async function walk(folder, relative = '') {
        for (const entry of await readdir(folder, { withFileTypes: true })) {
          const rel = path.posix.join(relative, entry.name);
          if (entry.isDirectory()) { await walk(path.join(folder, entry.name), rel); continue; }
          if (!/\.md(?:oc)?$/i.test(entry.name)) {
            await mkdir(path.join(destination, relative), { recursive: true });
            await copyFile(path.join(folder, entry.name), path.join(destination, rel));
            continue;
          }
          const route = /(?:^|\/)index\.md(?:oc)?$/i.test(rel) ? rel.replace(/index\.md(?:oc)?$/i, '') : rel.replace(/\.md(?:oc)?$/i, '/');
          const html = path.join(destination, route, 'index.html');
          let contents = await readFile(html, 'utf8');
          const origin = path.posix.dirname(product.sources[rel]);
          contents = contents.replace(/\b(href|src)="([^"]+)"/g, (match, attr, target) => {
            if (/^(?:[a-z][a-z\d+.-]*:|\/|#|\/\/)/i.test(target)) return match;
            const [pathname, suffix = ''] = target.split(/(?=[?#])/, 2);
            const resolved = path.posix.normalize(path.posix.join(origin, pathname));
            let local = resolved === 'README.md' ? '' : resolved.startsWith('docs/user/') ? resolved.slice(10) : null;
            if (local !== null) {
              if (/\.md(?:oc)?$/i.test(local)) local = local.replace(/(?:^|\/)README\.md(?:oc)?$/i, '/').replace(/\.md(?:oc)?$/i, '/');
              const result = `/${product.section}/${product.repo}/${local}`.replace(/\/{2,}/g, '/');
              return `${attr}="${result}${suffix}"`;
            }
            const kind = attr === 'src' ? 'raw' : 'blob';
            return `${attr}="https://github.com/qso-graph/${product.repo}/${kind}/${product.tag}/${resolved}${suffix}"`;
          });
          await writeFile(html, contents);
        }
      }
      await walk(source);
    }
  } } };
}
