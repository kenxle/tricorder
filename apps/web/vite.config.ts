import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The page reads JSON from the server (bin/serve, port 8787). In dev, Vite
// proxies /api and /trpc there. The build uses the same origin through bin/serve.
export default defineConfig({
  plugins: [react()],
  // Two pages: the readout, and steering's page until App.tsx mounts it.
  build: {
    rollupOptions: {
      input: {
        main: fileURLToPath(new URL("index.html", import.meta.url)),
        steer: fileURLToPath(new URL("steer.html", import.meta.url)),
      },
    },
  },
  server: {
    open: true,
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8787",
      "/health": "http://127.0.0.1:8787",
      "/trpc": "http://127.0.0.1:8787",
    },
  },
});
