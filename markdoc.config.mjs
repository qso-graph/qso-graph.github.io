import { defineMarkdocConfig, component } from '@astrojs/markdoc/config';
import starlightMarkdoc from '@astrojs/starlight-markdoc';

export default defineMarkdocConfig({
  extends: [starlightMarkdoc()],
  tags: {
    metric: { render: component('./src/components/Metric.astro'), attributes: { name: { type: String, required: true }, package: { type: String } }, selfClosing: true },
    'tool-reference': { render: component('./src/components/ToolReference.astro'), attributes: { repo: { type: String, required: true } }, selfClosing: true },
    'product-list': { render: component('./src/components/ProductList.astro'), selfClosing: true },
  },
});
