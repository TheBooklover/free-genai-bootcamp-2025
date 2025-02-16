import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import GroupWordsList from '../GroupWordsList';
import { fetchGroupWords } from '../../services/api';
import type { Mock } from 'vitest';

// Mock the API call
vi.mock('../../services/api', () => ({
  fetchGroupWords: vi.fn()
}));

const mockWords = {
  words: [
    { 
      id: 1, 
      quebecois: 'Bonjour', 
      standard_french: 'Bonjour', 
      english: 'Hello',
      created_at: '2024-02-15T10:00:00Z' 
    },
    { 
      id: 2, 
      quebecois: 'Au revoir', 
      standard_french: 'Au revoir', 
      english: 'Goodbye',
      created_at: '2024-02-15T11:00:00Z' 
    }
  ],
  total: 2,
  page: 1,
  per_page: 10,
  total_pages: 1
};

// Add pagination mock data
const mockPaginatedWords = {
  words: [
    { 
      id: 1, 
      quebecois: 'Bonjour', 
      standard_french: 'Bonjour', 
      english: 'Hello',
      created_at: '2024-02-15T10:00:00Z' 
    }
  ],
  total: 15,
  page: 1,
  per_page: 10,
  total_pages: 2
};

describe('GroupWordsList', () => {
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

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading state with skeleton rows', () => {
    render(<GroupWordsList groupId={1} />, { wrapper });

    // Check for skeleton rows
    const skeletonRows = screen.getAllByRole('row');
    expect(skeletonRows.length).toBe(11); // 10 data rows + 1 header row

    // Check for skeleton cells in first row
    const firstRow = skeletonRows[1];
    const skeletonCells = firstRow.querySelectorAll('.h-4');
    expect(skeletonCells.length).toBe(3); // Term, Definition, Added Date

    // Verify skeleton widths
    const [termSkeleton, defSkeleton, dateSkeleton] = Array.from(skeletonCells);
    expect(termSkeleton).toHaveClass('w-[100px]');
    expect(defSkeleton).toHaveClass('w-[200px]');
    expect(dateSkeleton).toHaveClass('w-[100px]');
  });

  it('displays words data correctly when loaded', async () => {
    // Setup mock response
    (fetchGroupWords as Mock).mockResolvedValueOnce(mockWords);

    // Render component
    render(<GroupWordsList groupId={1} />, { wrapper });

    // Wait for and verify data display
    await waitFor(() => {
      // Check if words are displayed
      expect(screen.getByText('Bonjour')).toBeInTheDocument();
      expect(screen.getByText('Au revoir')).toBeInTheDocument();

      // Check if dates are formatted correctly
      const formattedDate = new Date('2024-02-15T10:00:00Z').toLocaleDateString();
      expect(screen.getByText(formattedDate)).toBeInTheDocument();

      // Verify table structure
      const rows = screen.getAllByRole('row');
      expect(rows).toHaveLength(3); // Header + 2 data rows

      // Verify API call
      expect(fetchGroupWords).toHaveBeenCalledWith(
        1,
        1,
        10,
        'quebecois',
        'asc'
      );
    });
  });

  it('displays error state when API call fails', async () => {
    // Setup mock error
    const errorMessage = 'Failed to fetch words';
    (fetchGroupWords as any).mockRejectedValueOnce(new Error(errorMessage));

    // Render component
    render(<GroupWordsList groupId={1} />, { wrapper });

    // Wait for and verify error display
    await waitFor(() => {
      // Check if error message is displayed
      expect(screen.getByText(`Error loading words: ${errorMessage}`)).toBeInTheDocument();

      // Verify error styling
      const errorElement = screen.getByText(/Error loading words/);
      expect(errorElement.parentElement).toHaveClass('text-red-500');

      // Verify error is contained in a Card
      expect(errorElement.closest('.card')).toBeInTheDocument();

      // Verify table is not rendered when in error state
      expect(screen.queryByRole('table')).not.toBeInTheDocument();
    });

    // Verify API was called with correct parameters
    expect(fetchGroupWords).toHaveBeenCalledWith(
      1,
      1,
      10,
      'quebecois',
      'asc'
    );
  });

  describe('pagination', () => {
    it('renders pagination controls correctly', async () => {
      // Setup mock response
      (fetchGroupWords as any).mockResolvedValueOnce(mockPaginatedWords);
      
      render(<GroupWordsList groupId={1} />, { wrapper });

      await waitFor(() => {
        // Verify pagination text
        expect(screen.getByText('Page 1 of 2')).toBeInTheDocument();
        
        // Verify navigation buttons
        const prevButton = screen.getByText('Previous');
        const nextButton = screen.getByText('Next');
        expect(prevButton).toBeInTheDocument();
        expect(nextButton).toBeInTheDocument();
        
        // Verify initial button states
        expect(prevButton).toBeDisabled();
        expect(nextButton).not.toBeDisabled();
      });
    });

    it('handles page navigation correctly', async () => {
      // Setup sequential mock responses
      (fetchGroupWords as any)
        .mockResolvedValueOnce({
          ...mockPaginatedWords,
          page: 1
        })
        .mockResolvedValueOnce({
          ...mockPaginatedWords,
          page: 2,
          words: [{ 
            id: 2, 
            quebecois: 'Au revoir', 
            standard_french: 'Au revoir', 
            english: 'Goodbye',
            created_at: '2024-02-15T11:00:00Z' 
          }]
        });

      render(<GroupWordsList groupId={1} />, { wrapper });

      // Wait for initial render
      await waitFor(() => {
        expect(screen.getByText('Bonjour')).toBeInTheDocument();
      });

      // Click next page
      const nextButton = screen.getByText('Next');
      fireEvent.click(nextButton);

      // Verify second page data is fetched
      await waitFor(() => {
        expect(fetchGroupWords).toHaveBeenCalledWith(
          1,
          2,
          10,
          'quebecois',
          'asc'
        );
        expect(screen.getByText('Au revoir')).toBeInTheDocument();
      });

      // Verify button states on last page
      await waitFor(() => {
        expect(screen.getByText('Previous')).not.toBeDisabled();
        expect(screen.getByText('Next')).toBeDisabled();
      });
    });

    it('maintains current page data while loading next page', async () => {
      // Setup mock with delay
      (fetchGroupWords as any)
        .mockResolvedValueOnce({
          ...mockPaginatedWords,
          page: 1
        })
        .mockImplementationOnce(() => 
          new Promise(resolve => 
            setTimeout(() => 
              resolve({
                ...mockPaginatedWords,
                page: 2,
                words: [{ 
                  id: 2, 
                  quebecois: 'Au revoir', 
                  standard_french: 'Au revoir', 
                  english: 'Goodbye',
                  created_at: '2024-02-15T11:00:00Z' 
                }]
              }), 
              100
            )
          )
        );

      render(<GroupWordsList groupId={1} />, { wrapper });

      // Wait for initial render
      await waitFor(() => {
        expect(screen.getByText('Bonjour')).toBeInTheDocument();
      });

      // Click next page
      fireEvent.click(screen.getByText('Next'));

      // Verify current data remains visible during loading
      expect(screen.getByText('Bonjour')).toBeInTheDocument();
      expect(screen.queryByText('Au revoir')).not.toBeInTheDocument();

      // Verify new data appears after loading
      await waitFor(() => {
        expect(screen.getByText('Au revoir')).toBeInTheDocument();
        expect(screen.queryByText('Bonjour')).not.toBeInTheDocument();
      });
    });
  });

  describe('sorting', () => {
    it('updates sort icons when clicking column headers', async () => {
      (fetchGroupWords as any).mockResolvedValueOnce(mockWords);
      
      render(<GroupWordsList groupId={1} />, { wrapper });

      // Wait for initial render
      await waitFor(() => {
        expect(screen.getByText('Bonjour')).toBeInTheDocument();
      });

      // Get all sortable column headers
      const termButton = screen.getByRole('button', { name: /Term/i });
      const definitionButton = screen.getByRole('button', { name: /Definition/i });
      const dateButton = screen.getByRole('button', { name: /Added Date/i });

      // Initially, Term column should show ascending icon
      expect(termButton.querySelector('.lucide-arrow-up')).toBeInTheDocument();

      // Click Term column to change to descending
      fireEvent.click(termButton);
      expect(termButton.querySelector('.lucide-arrow-down')).toBeInTheDocument();

      // Click Definition column to sort by it
      fireEvent.click(definitionButton);
      expect(definitionButton.querySelector('.lucide-arrow-up')).toBeInTheDocument();
      expect(termButton.querySelector('.lucide-arrows-up-down')).toBeInTheDocument();
    });

    it('fetches data with correct sort parameters', async () => {
      (fetchGroupWords as any).mockResolvedValue(mockWords);
      
      render(<GroupWordsList groupId={1} />, { wrapper });

      // Wait for initial render
      await waitFor(() => {
        expect(fetchGroupWords).toHaveBeenCalledWith(
          1, 1, 10, 'quebecois', 'asc'
        );
      });

      // Click Term column to sort descending
      const termButton = screen.getByRole('button', { name: /Term/i });
      fireEvent.click(termButton);

      await waitFor(() => {
        expect(fetchGroupWords).toHaveBeenCalledWith(
          1, 1, 10, 'quebecois', 'desc'
        );
      });

      // Click Definition column to sort ascending
      const definitionButton = screen.getByRole('button', { name: /Definition/i });
      fireEvent.click(definitionButton);

      await waitFor(() => {
        expect(fetchGroupWords).toHaveBeenCalledWith(
          1, 1, 10, 'standard_french', 'asc'
        );
      });
    });

    it('maintains sort state when changing pages', async () => {
      (fetchGroupWords as any)
        .mockResolvedValueOnce({
          ...mockPaginatedWords,
          page: 1
        })
        .mockResolvedValueOnce({
          ...mockPaginatedWords,
          page: 2
        });

      render(<GroupWordsList groupId={1} />, { wrapper });

      // Sort by Definition descending
      const definitionButton = screen.getByRole('button', { name: /Definition/i });
      fireEvent.click(definitionButton);
      fireEvent.click(definitionButton);

      await waitFor(() => {
        expect(fetchGroupWords).toHaveBeenCalledWith(
          1, 1, 10, 'standard_french', 'desc'
        );
      });

      // Change page
      const nextButton = screen.getByText('Next');
      fireEvent.click(nextButton);

      // Verify sort parameters are maintained
      await waitFor(() => {
        expect(fetchGroupWords).toHaveBeenCalledWith(
          1, 2, 10, 'standard_french', 'desc'
        );
      });
    });
  });
}); 