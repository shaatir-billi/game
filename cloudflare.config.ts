import { defineConfig, bindings } from "cf/config";
export default defineConfig({
  accountId: "7ae1de37f9adbd35d53ec81b6c1cb99b",
  worker: {
    name: "shaatir-billi",
    compatibilityDate: "2026-10-13",
    entrypoint: "./worker/index.js",
    domains: ["shaatirbilli.mhadi.dev"],
    assets: { notFoundHandling: "none" },
    env: { ASSETS: bindings.assets() },
    observability: { enabled: true, traces: { enabled: true } },
  },
});
