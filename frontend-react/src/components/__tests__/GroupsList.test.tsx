import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import GroupsList from '../GroupsList';
import { fetchGroups } from '../../services/api';

// Mock the API call
vi.mock('../../services/api', () => ({
  fetchGroups: vi.fn(),
}));

// Mock date formatting to avoid timezone issues in tests
vi.mock('../../lib/utils', () => ({
  formatDate: (date: string) => new Date(date).toLocaleDateString(),
}));

// Setup QueryClient for tests
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    {children}
  </QueryClientProvider>
);

const mockGroups = {
  groups: [
    {
      id: 1,
      name: "Common Verbs",
      word_count: 25,
      created_at: "2024-02-15T10:00:00Z",
      updated_at: "2024-02-15T10:00:00Z"
    },
    {
      id: 2,
      name: "Basic Nouns",
      word_count: 30,
      created_at: "2024-02-14T10:00:00Z",
      updated_at: "2024-02-14T10:00:00Z"
    }
  ],
  total: 2,
  page: 1,
  per_page: 10,
  total_pages: 1
};

describe('GroupsList', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    queryClient.clear();
  });

  it('shows loading state initially', () => {
    (fetchGroups as any).mockImplementation(() => new Promise(() => {}));
    
    render(<GroupsList />, { wrapper });
    
    expect(screen.getAllByTestId('skeleton-row')).toHaveLength(10);
  });

  it('displays groups data when loaded', async () => {
    (fetchGroups as any).mockResolvedValue(mockGroups);
    
    render(<GroupsList />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText('Common Verbs')).toBeInTheDocument();
      expect(screen.getByText('Basic Nouns')).toBeInTheDocument();
      expect(screen.getByText('25')).toBeInTheDocument();
      expect(screen.getByText('30')).toBeInTheDocument();
    });
  });

  it('handles error state', async () => {
    const errorMessage = 'Failed to fetch groups';
    (fetchGroups as any).mockRejectedValue(new Error(errorMessage));
    
    render(<GroupsList />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText(`Error loading groups: ${errorMessage}`)).toBeInTheDocument();
    });
  });

  it('handles sorting', async () => {
    (fetchGroups as any).mockResolvedValue(mockGroups);
    
    render(<GroupsList />, { wrapper });
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Common Verbs')).toBeInTheDocument();
    });

    // Click name header to sort
    fireEvent.click(screen.getByText('Name'));
    
    await waitFor(() => {
      expect(fetchGroups).toHaveBeenCalledWith(
        expect.anything(),
        expect.anything(),
        'name',
        'desc'
      );
    });
  });

  it('handles pagination', async () => {
    const multiPageGroups = {
      ...mockGroups,
      total_pages: 2,
      total: 4
    };
    
    (fetchGroups as any).mockResolvedValue(multiPageGroups);
    
    render(<GroupsList />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText('Page 1 of 2')).toBeInTheDocument();
    });

    // Click next page
    fireEvent.click(screen.getByText('Next'));
    
    await waitFor(() => {
      expect(fetchGroups).toHaveBeenCalledWith(2, expect.anything(), expect.anything(), expect.anything());
    });
  });

  it('disables pagination buttons appropriately', async () => {
    (fetchGroups as any).mockResolvedValue(mockGroups);
    
    render(<GroupsList />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText('Previous')).toBeDisabled();
      expect(screen.getByText('Next')).toBeDisabled();
    });
  });
}); 