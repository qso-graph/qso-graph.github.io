import {readFileSync, writeFileSync} from 'node:fs';
const servers = Object.values(JSON.parse(readFileSync('data/servers.json', 'utf8')));
const text = readFileSync('src/data/llms.txt', 'utf8').replaceAll('{{ server_count() }}', String(servers.filter(s => s.kind === 'server').length)).replaceAll('{{ tool_total() }}', String(servers.reduce((n,s) => n + s.tools.length, 0)));
writeFileSync('public/llms.txt', text);
