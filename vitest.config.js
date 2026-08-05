import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['tests/js/**/*.test.js'],
    coverage: {
      provider: 'v8',
      include: ['insight_ui/static/insight_ui/js/**/*.js'],
      exclude: ['**/*.test.js'],
      reporter: ['text', 'html'],
    },
    setupFiles: ['./tests/js/setup.js'],
  },
});
