import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

// The page reads JSON from the server (bin/serve, port 8787). In dev, Vite
// proxies /api there. The build is served by the same server, so the demo
// needs one process and no CDN.
export default defineConfig({
  plugins: [react()],
  // Two pages: the readout, and steering's page until App.tsx mounts it.
  build: {
    rollupOptions: {
      input: {
        main: fileURLToPath(new URL("./index.html", import.meta.url)),
        steer: fileURLToPath(new URL("./steer.html", import.meta.url)),
      },
    },
  },
  server: {
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:8787", "/health": "http://127.0.0.1:8787" },
    fs: { allow: [".."] },
  },
});
