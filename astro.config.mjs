import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';
import redirects from './redirects.json' with { type: 'json' };
import productLinks from './integrations/product-links.mjs';
import { existsSync, readFileSync } from 'node:fs';

// What the fetcher wrote (scripts/fetch_docs.py): each product's section and its files. A product
// with only its README is one link; one with docs/user/ pages is a group of them. Before the first
// fetch there are none, and the sections are empty.
const products = existsSync('./data/docs.json') ? JSON.parse(readFileSync('./data/docs.json', 'utf8')) : [];
const SECTIONS = [['applications', 'Applications'], ['mcp-servers', 'MCP Servers'], ['libraries', 'Libraries'], ['tools', 'Tools']];
const productItems = (section) => products
  .filter((p) => p.section === section)
  .sort((a, b) => a.repo.localeCompare(b.repo))
  .map((p) => Object.keys(p.sources).length > 1
    ? { label: p.repo, collapsed: true, items: [{ autogenerate: { directory: `${section}/${p.repo}` } }] }
    : { label: p.repo, link: `/${section}/${p.repo}/` });

export default defineConfig({
  site: 'https://qso-graph.io',
  redirects,
  integrations: [starlight({
    title: 'QSO Graph',
    favicon: '/assets/images/favicon.png',
    customCss: ['./src/styles/custom.css'],
    components: {
      MarkdownContent: './src/components/MarkdownContent.astro',
      Head: './src/components/Head.astro',
      PageFrame: './src/components/PageFrame.astro',
      TwoColumnContent: './src/components/TwoColumnContent.astro',
    },
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/qso-graph/qso-graph.github.io' }],
    sidebar: [
      { label: 'Home', link: '/' },
      { label: 'Products', link: '/products/' },
      { label: 'Specification', link: '/specification/' },
      // Every group starts collapsed and opens when clicked; the group holding the page being read
      // opens on its own, so the reader always sees where they are.
      ...SECTIONS.map(([section, label]) => ({ label, collapsed: true, items: productItems(section) })),
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
