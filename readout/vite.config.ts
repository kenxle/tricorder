import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The page reads JSON from the server (bin/serve, port 8787). In dev, Vite
// proxies /api there. The build is served by the same server, so the demo
// needs one process and no CDN.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:8787", "/health": "http://127.0.0.1:8787" },
    fs: { allow: [".."] },
  },
});
