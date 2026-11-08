import productLinks from './scripts/remark-product-links.mjs';
import {readFileSync} from 'node:fs';
const redirects = JSON.parse(readFileSync('./redirects.json'));
export default {
  title: 'QSO Graph', url: 'https://qso-graph.io', baseUrl: '/', trailingSlash: true,
  favicon: 'favicon.png', staticDirectories: ['public'], onBrokenLinks: 'throw',
  i18n: {defaultLocale: 'en', locales: ['en']},
  markdown: {format: 'detect', hooks: {onBrokenMarkdownLinks: 'throw'}},
  presets: [['classic', {docs: {path: 'src/content/docs', routeBasePath: '/', sidebarPath: './sidebars.mjs', sidebarCollapsed: true, beforeDefaultRemarkPlugins: [productLinks]}, blog: false, theme: {customCss: './src/styles/custom.css'}}]],
  plugins: [['@docusaurus/plugin-client-redirects', {redirects: Object.entries(redirects).map(([from,to]) => ({from,to}))}]],
  themes: [['@easyops-cn/docusaurus-search-local', {hashed: true, indexDocs: true, indexBlog: false, docsDir: 'src/content/docs', docsRouteBasePath: '/', indexPages: false, language: ['en']}]],
  themeConfig: {
    image: 'assets/social-card.png',
    navbar: {title: 'QSO Graph', logo: {alt: '', src: 'assets/qso-graph-icon.png'}, items: [{href: 'https://github.com/qso-graph/qso-graph.github.io', label: 'GitHub', position: 'right'}]},
    docs: {sidebar: {hideable: true}},
    colorMode: {respectPrefersColorScheme: true},
    metadata: [{name: 'theme-color', content: '#ffffff'}],
  },
  headTags: [{tagName: 'link', attributes: {rel: 'apple-touch-icon', href: '/apple-touch-icon.png'}}],
};
