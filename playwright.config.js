const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  timeout: 30000,
  use: {
    baseURL: 'https://vladimirmakarov82.github.io/pulse',
    headless: true,
  },
});
