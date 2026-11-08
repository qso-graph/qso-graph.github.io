import {readFileSync, existsSync} from 'node:fs';
const products = existsSync('./data/docs.json') ? JSON.parse(readFileSync('./data/docs.json')) : [];
const docId = (p, file) => `${p.section}/${p.repo}/${file.replace(/\.(md|mdoc|mdx)$/i, '')}`;
const items = (section) => products.filter(p => p.section === section).sort((a,b) => a.repo.localeCompare(b.repo)).map(p => {
  const docs = Object.keys(p.sources).sort((a,b) => a === 'index.md' ? -1 : b === 'index.md' ? 1 : a.localeCompare(b));
  return docs.length === 1 ? {type:'doc', id:docId(p, docs[0]), label:p.repo} : {type:'category', label:p.repo, collapsed:true, items:docs.map(file => ({type:'doc', id:docId(p,file), ...(file === 'index.md' ? {label:'Overview'} : {})}))};
});
export default {docs: [
  {type:'doc', id:'index', label:'Home'}, 'products', 'specification',
  ...[['applications','Applications'],['mcp-servers','MCP Servers'],['libraries','Libraries'],['tools','Tools']].map(([section,label]) => ({type:'category', label, collapsed:true, items:[...(section === 'mcp-servers' ? [{type:'doc',id:'servers/index',label:'Overview'}] : []), ...items(section)]})).filter(x => x.items.length),
  {type:'doc', id:'getting-started', label:'Getting Started'}, {type:'doc', id:'credentials', label:'Credential Setup'}, {type:'doc', id:'architecture', label:'Architecture'}, {type:'doc', id:'testing', label:'Testing'}, {type:'doc', id:'security', label:'Security'},
  {type:'category', label:'About', collapsed:true, items:['about/index','about/contributing','about/attributions']},
]};
