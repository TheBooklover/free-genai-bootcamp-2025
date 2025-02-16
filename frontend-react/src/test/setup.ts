import '@testing-library/jest-dom';
import { expect, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect method
expect.extend(matchers);

// Cleanup after each test case
beforeEach(() => {
    cleanup();
});

afterEach(() => {
  vi.clearAllMocks();
});

// Use node-fetch instead of @remix-run/web-fetch
import fetch from 'node-fetch';
global.fetch = fetch as any;

vi.mock('@tanstack/react-query', () => ({
  useQuery: vi.fn(),
  QueryClient: vi.fn(() => ({
    setDefaultOptions: vi.fn(),
  })),
  QueryClientProvider: ({ children }: { children: React.ReactNode }) => children,
})); 