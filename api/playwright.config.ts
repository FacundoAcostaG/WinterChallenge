import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  fullyParallel: true,
  retries: 0,
  reporter: [['list']],
  outputDir: 'api/test-results',
  use: {
    extraHTTPHeaders: {
      Accept: 'application/json'
    }
  }
});
