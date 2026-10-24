import { defineConfig } from "oxfmt";
import ultracite from "ultracite/oxfmt";

export default defineConfig({
  ...ultracite,
  ignorePatterns: [
    ...ultracite.ignorePatterns,
    "docs/**",
    "memo/**",
    "scans/**",
    "schema/**",
    "pyproject.toml",
    "data_room/**",
    "sample_out/**",
    "schema/claim.schema.json",
    "server/openapi.json",
    "packages/schema/src/api.ts",
    "packages/schema/src/claim.ts",
    "apps/mobile/ios/**",
    "apps/mobile/android/**",
    "apps/mobile/expo-env.d.ts",
    ".venv/**",
    ".agents/**",
    ".claude/**",
    ".codex/**",
  ],
});
