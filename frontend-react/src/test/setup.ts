import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect method
expect.extend(matchers);

// Cleanup after each test case
afterEach(() => {
    cleanup();
});

// Use node-fetch instead of @remix-run/web-fetch
import fetch from 'node-fetch';
global.fetch = fetch as any; 