import { ReactElement } from 'react';
import { render, RenderResult } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const createTestQueryClient = () => new QueryClient({
    defaultOptions: {
        queries: {
            retry: false,
        },
    },
});

export function renderWithClient(ui: ReactElement): RenderResult {
    const testQueryClient = createTestQueryClient();
    return render(ui as React.ReactNode);
}

export * from '@testing-library/react'; 