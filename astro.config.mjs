import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';
import redirects from './redirects.json' with { type: 'json' };
import productLinks from './integrations/product-links.mjs';

export default defineConfig({
  site: 'https://qso-graph.io',
  redirects,
  integrations: [starlight({
    title: 'QSO Graph',
    favicon: '/assets/images/favicon.png',
    customCss: ['./src/styles/custom.css'],
    components: { MarkdownContent: './src/components/MarkdownContent.astro' },
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/qso-graph/qso-graph.github.io' }],
    sidebar: [
      { label: 'Home', link: '/' },
      { label: 'Products', link: '/products/' },
      { label: 'Specification', link: '/specification/' },
      // Every group starts collapsed and opens when clicked; the group holding the page being read
      // opens on its own, so the reader always sees where they are.
      ...['applications', 'mcp-servers', 'libraries', 'tools'].map((directory, i) => ({ label: ['Applications', 'MCP Servers', 'Libraries', 'Tools'][i], collapsed: true, items: [{ autogenerate: { directory, collapsed: true } }] })),
      { label: 'MCP Servers overview', link: '/servers/' },
      { label: 'Getting Started', link: '/getting-started/' },
      { label: 'Credential Setup', link: '/credentials/' },
      { label: 'Architecture', link: '/architecture/' },
      { label: 'Testing', link: '/testing/' },
      { label: 'Security', link: '/security/' },
      { label: 'About', collapsed: true, items: [{ autogenerate: { directory: 'about', collapsed: true } }] },
    ],
  }), markdoc(), productLinks()],
});
