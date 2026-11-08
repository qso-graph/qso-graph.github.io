import React from 'react';
import products from '@site/data/docs.json';
import servers from '@site/data/servers.json';
export function Metric({name, package: pkg}) {
  const s = servers[pkg];
  if (pkg && !s) throw new Error(`Missing package data: ${pkg}`);
  const values = {server_count: () => Object.values(servers).filter(s => s.kind === 'server').length, tool_total: () => Object.values(servers).reduce((n,s) => n + s.tools.length, 0), version: () => s.version, tools: () => s.tools.length, ci_badge: () => <a href={`https://github.com/qso-graph/${s.repo}/actions/workflows/ci.yml`}><img alt="CI" src={`https://github.com/qso-graph/${s.repo}/actions/workflows/ci.yml/badge.svg`} /></a>};
  if (!values[name]) throw new Error(`Unknown metric: ${name}`);
  return values[name]();
}
export function Products() {
  return <>{[['applications','Applications'],['mcp-servers','MCP Servers'],['libraries','Libraries'],['tools','Tools']].map(([section,title]) => <React.Fragment key={section}><h2 id={section}>{title}</h2><table><thead><tr><th>Product</th><th>What it is</th><th>Version</th></tr></thead><tbody>{products.filter(p => p.sections.includes(section)).sort((a,b) => a.repo.localeCompare(b.repo)).map(p => <tr key={p.repo} id={p.section === section ? p.repo : `${section}-${p.repo}`}><td><a href={`/${p.section}/${p.repo}/`}>{p.repo}</a></td><td>{p.description}</td><td><a href={`https://github.com/qso-graph/${p.repo}/releases/tag/${encodeURIComponent(p.tag)}`}>{p.tag}</a></td></tr>)}</tbody></table></React.Fragment>)}</>;
}
