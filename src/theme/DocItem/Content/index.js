import React from 'react';
import Content from '@theme-original/DocItem/Content';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import products from '@site/data/docs.json';
import servers from '@site/data/servers.json';
function type(s) { if (s.anyOf) return s.anyOf.filter(x => x.type !== 'null').map(type).join(' or ') || 'null'; if (s.enum) return s.enum.join(' / '); if (s.type === 'array') return `list of ${type(s.items || {})}`; return s.type || 'any'; }
function description(text) { let section = ''; return text.split('\n').filter(line => {const m = line.match(/^(Args|Arguments|Parameters|Returns|Raises|Example|Examples):\s*$/); if (m) {section = m[1]; return section === 'Returns';} return !section || section === 'Returns';}).join('\n').trim(); }
function ToolReference({product}) {
 const server = Object.values(servers).find(s => s.repo === product.repo);
 if (!server || product.tag !== `v${server.version}` || server.kind !== 'server') throw new Error(`${product.repo}: missing matching released server data`);
 return <><hr/><h2 id="tool-reference">Tool Reference</h2><p>Generated from the released server's own tool definitions.</p>{server.tool_details.map(t => <section key={t.name}><h3 id={t.name}>{t.name}</h3>{description(t.description).split(/\n\s*\n/).filter(Boolean).map((p,i) => <p key={i} style={{whiteSpace:'pre-line'}}>{p}</p>)}{Object.keys(t.inputSchema.properties || {}).length ? <table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Default</th><th>Description</th></tr></thead><tbody>{(t.params?.length ? t.params : Object.keys(t.inputSchema.properties)).map(name => {const s=t.inputSchema.properties[name], required=(t.inputSchema.required || []).includes(name); return <tr key={name}><td><code>{name}</code></td><td>{type(s)}</td><td>{required ? 'Yes':'No'}</td><td>{!required && 'default' in s ? <code>{JSON.stringify(s.default)}</code> : ''}</td><td>{s.description || ''}</td></tr>;})}</tbody></table> : <p>No parameters.</p>}</section>)}</>;
}
export default function ContentWrapper(props) {
 const {metadata} = useDoc();
 const p = products.find(p => metadata.id.startsWith(`${p.section}/${p.repo}/`));
 const file = p && metadata.source.split(`/${p.section}/${p.repo}/`)[1];
 const source = p && p.sources[file];
 return <>{source && <div className="alert alert--secondary margin-bottom--lg">Documentation for <strong>{p.repo} {p.tag}</strong>. <a href={`https://github.com/qso-graph/${p.repo}/blob/${p.tag}/${source}`}>Source at {p.tag}</a>.</div>}<Content {...props}/>{source === 'README.md' && p.section === 'mcp-servers' && <div className="markdown"><ToolReference product={p}/></div>}</>;
}
