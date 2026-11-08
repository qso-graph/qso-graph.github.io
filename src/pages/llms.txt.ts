import template from '../data/llms.txt?raw';
import servers from '../../data/servers.json';

export function GET() {
  const count = Object.values(servers).filter((server) => server.kind === 'server').length;
  const total = Object.values(servers).reduce((sum, server) => sum + server.tools.length, 0);
  const text = template
    .replaceAll('{{ server_count() }}', String(count)).replaceAll('{{ tool_total() }}', String(total));
  return new Response(text, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
