import {readFile, readdir, mkdir, copyFile} from 'node:fs/promises';
import path from 'node:path';
const products = JSON.parse(await readFile('data/docs.json', 'utf8'));
for (const p of products) {
 const root = path.join('src/content/docs', p.section, p.repo);
 async function copy(dir, rel = '') {
  for (const entry of await readdir(dir, {withFileTypes: true})) {
   const name = path.join(rel, entry.name), source = path.join(dir, entry.name);
   if (entry.isDirectory()) await copy(source, name);
   else if (!/\.md(?:oc|x)?$/i.test(name)) {const dest = path.join('build', p.section, p.repo, name); await mkdir(path.dirname(dest), {recursive:true}); await copyFile(source, dest);}
  }
 }
 await copy(root);
}
