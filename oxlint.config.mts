import { defineConfig } from "oxlint";
import core from "ultracite/oxlint/core";
import react from "ultracite/oxlint/react";

export default defineConfig({
  env: core.env,
  extends: [core, react],
  ignorePatterns: [
    ...core.ignorePatterns,
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
  // Incremental migration: only pre-existing files waive their existing violations.
  // New files inherit the full presets. Remove a file/rule exception when fixing it.
  // See docs/ongoing/TESTING.md. Do not add exceptions to make new code pass.
  overrides: [
    {
      files: ["apps/mobile/src/app/index.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/eslint.config.js"],
      rules: {
        "unicorn/prefer-module": "off",
      },
    },
    {
      files: ["apps/mobile/scripts/reset-project.js"],
      rules: {
        "eslint/no-await-in-loop": "off",
        "promise/catch-or-return": "off",
        "unicorn/prefer-module": "off",
      },
    },
    {
      files: ["apps/mobile/src/app/_layout.tsx"],
      rules: {
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/src/app/explore.tsx"],
      rules: {
        "eslint/no-use-before-define": "off",
        "node/global-require": "off",
        "react/function-component-definition": "off",
        "unicorn/prefer-module": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/animated-icon.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "node/global-require": "off",
        "promise/catch-or-return": "off",
        "react/function-component-definition": "off",
        "unicorn/prefer-module": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/animated-icon.web.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "node/global-require": "off",
        "react/function-component-definition": "off",
        "unicorn/prefer-module": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/app-tabs.tsx"],
      rules: {
        "node/global-require": "off",
        "react/function-component-definition": "off",
        "unicorn/prefer-module": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/app-tabs.web.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/external-link.tsx"],
      rules: {
        "eslint/func-style": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/hint-row.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/themed-text.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/themed-view.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-unused-vars": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/ui/collapsible.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/src/components/web-badge.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "node/global-require": "off",
        "react/function-component-definition": "off",
        "unicorn/prefer-module": "off",
      },
    },
    {
      files: ["apps/mobile/src/hooks/use-color-scheme.web.ts"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-empty-function": "off",
      },
    },
    {
      files: ["apps/mobile/src/hooks/use-theme.ts"],
      rules: {
        "eslint/func-style": "off",
      },
    },
    {
      files: ["apps/mobile/src/prototype/FlowScreen.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-nested-ternary": "off",
        "eslint/no-use-before-define": "off",
        "react/exhaustive-effect-dependencies": "off",
        "react/function-component-definition": "off",
        "unicorn/filename-case": "off",
      },
    },
    {
      files: ["apps/mobile/src/readout/FounderRequests.tsx"],
      rules: {
        "eslint/complexity": "off",
        "eslint/func-style": "off",
        "eslint/no-await-in-loop": "off",
        "eslint/no-nested-ternary": "off",
        "eslint/no-use-before-define": "off",
        "eslint/prefer-named-capture-group": "off",
        "eslint/require-await": "off",
        "eslint/require-unicode-regexp": "off",
        "promise/always-return": "off",
        "promise/no-callback-in-promise": "off",
        "react/exhaustive-effect-dependencies": "off",
        "react/function-component-definition": "off",
        "react/todo": "off",
        "unicorn/filename-case": "off",
      },
    },
    {
      files: ["apps/mobile/src/readout/ReadoutScreen.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-plusplus": "off",
        "eslint/no-use-before-define": "off",
        "eslint/no-void": "off",
        "promise/always-return": "off",
        "promise/catch-or-return": "off",
        "react-hooks/exhaustive-deps": "off",
        "react/exhaustive-effect-dependencies": "off",
        "react/function-component-definition": "off",
        // Preserve the existing external-data effect suppression after formatting.
        "react/rule-suppression": "off",
        "react/set-state-in-effect": "off",
        "react/todo": "off",
        "unicorn/filename-case": "off",
        "unicorn/no-array-for-each": "off",
      },
    },
    {
      files: ["apps/mobile/src/readout/SourceChip.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "eslint/no-void": "off",
        "oxc/branches-sharing-code": "off",
        "react/function-component-definition": "off",
        "react/todo": "off",
        "unicorn/filename-case": "off",
      },
    },
    {
      files: ["apps/mobile/src/readout/Steering.tsx"],
      rules: {
        "eslint/complexity": "off",
        "eslint/func-style": "off",
        "eslint/no-nested-ternary": "off",
        "eslint/no-shadow": "off",
        "eslint/no-use-before-define": "off",
        "eslint/no-void": "off",
        "eslint/prefer-named-capture-group": "off",
        "eslint/require-unicode-regexp": "off",
        "react/function-component-definition": "off",
        "react/hook-use-state": "off",
        "react/todo": "off",
        "typescript/no-non-null-assertion": "off",
        "unicorn/filename-case": "off",
        "unicorn/no-array-for-each": "off",
      },
    },
    {
      files: ["apps/mobile/src/readout/api.ts"],
      rules: {
        "eslint/func-style": "off",
        "eslint/require-unicode-regexp": "off",
      },
    },
    {
      files: ["apps/mobile/src/readout/proxy.ts"],
      rules: {
        "eslint/complexity": "off",
        "eslint/func-style": "off",
        "eslint/require-unicode-regexp": "off",
        "unicorn/no-lonely-if": "off",
      },
    },
    {
      files: ["apps/mobile/src/readout/ui.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-nested-ternary": "off",
        "eslint/no-use-before-define": "off",
        "react/function-component-definition": "off",
      },
    },
    {
      files: ["apps/mobile/tests/proxy.test.mjs"],
      rules: {
        "eslint/no-await-in-loop": "off",
        "eslint/require-await": "off",
        "unicorn/consistent-function-scoping": "off",
        "unicorn/no-await-expression-member": "off",
      },
    },
    {
      files: ["apps/rpc/src/router.ts"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-nested-ternary": "off",
        "eslint/prefer-named-capture-group": "off",
        "eslint/require-unicode-regexp": "off",
        "eslint/sort-keys": "off",
        "typescript/no-dynamic-delete": "off",
      },
    },
    {
      files: ["apps/rpc/src/server.test.ts"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-await-in-loop": "off",
        "eslint/require-await": "off",
        "promise/avoid-new": "off",
        "promise/prefer-await-to-callbacks": "off",
        "unicorn/new-for-builtins": "off",
        "unicorn/no-array-sort": "off",
      },
    },
    {
      files: ["apps/rpc/src/server.ts"],
      rules: {
        "eslint/func-style": "off",
        "eslint/prefer-named-capture-group": "off",
        "eslint/require-unicode-regexp": "off",
      },
    },
    {
      files: ["apps/web/src/App.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "promise/always-return": "off",
        "promise/prefer-await-to-callbacks": "off",
        "react/button-has-type": "off",
        "react/function-component-definition": "off",
        "react/set-state-in-effect": "off",
        "unicorn/consistent-function-scoping": "off",
        "unicorn/filename-case": "off",
      },
    },
    {
      files: ["apps/web/src/FounderRequests.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-inline-comments": "off",
        "eslint/no-nested-ternary": "off",
        "eslint/no-use-before-define": "off",
        "eslint/require-unicode-regexp": "off",
        "jsx-a11y/prefer-tag-over-role": "off",
        "promise/always-return": "off",
        "promise/catch-or-return": "off",
        "promise/prefer-catch": "off",
        "react/button-has-type": "off",
        "react/exhaustive-effect-dependencies": "off",
        "react/function-component-definition": "off",
        "react/no-unescaped-entities": "off",
        "react/set-state-in-effect": "off",
        "react/todo": "off",
        "typescript/no-non-null-assertion": "off",
        "unicorn/consistent-function-scoping": "off",
        "unicorn/filename-case": "off",
        "unicorn/prefer-code-point": "off",
      },
    },
    {
      files: ["apps/web/src/Steering.tsx"],
      rules: {
        "eslint/func-style": "off",
        "eslint/no-use-before-define": "off",
        "eslint/prefer-named-capture-group": "off",
        "eslint/require-unicode-regexp": "off",
        "jsx-a11y/prefer-tag-over-role": "off",
        "promise/always-return": "off",
        "promise/catch-or-return": "off",
        "promise/prefer-await-to-callbacks": "off",
        "promise/prefer-catch": "off",
        "react/button-has-type": "off",
        "react/function-component-definition": "off",
        "react/no-unescaped-entities": "off",
        "react/set-state-in-effect": "off",
        "unicorn/filename-case": "off",
      },
    },
    {
      files: ["apps/web/src/api.ts"],
      rules: {
        "eslint/func-style": "off",
      },
    },
    {
      files: ["apps/web/src/main.tsx"],
      rules: {
        "typescript/no-non-null-assertion": "off",
      },
    },
    {
      files: ["apps/web/src/steerApi.ts"],
      rules: {
        "eslint/func-style": "off",
        "unicorn/filename-case": "off",
      },
    },
    {
      files: ["apps/web/src/steer_main.tsx"],
      rules: {
        "eslint/func-style": "off",
        "promise/catch-or-return": "off",
        "promise/prefer-catch": "off",
        "react/function-component-definition": "off",
        "react/set-state-in-effect": "off",
        "typescript/no-non-null-assertion": "off",
        "unicorn/filename-case": "off",
      },
    },
    {
      files: ["apps/web/vite.config.ts"],
      rules: {
        "eslint/sort-keys": "off",
      },
    },
  ],
});
