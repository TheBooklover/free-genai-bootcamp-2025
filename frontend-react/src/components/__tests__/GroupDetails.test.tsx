import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import GroupDetails from '../GroupDetails';
import { fetchGroupDetails } from '../../services/api';
import { renderWithClient } from '../../test/utils';

// Mock the API call
vi.mock('../../services/api', () => ({
  fetchGroupDetails: vi.fn(),
}));

const mockGroup = {
  id: 1,
  name: "Common Verbs",
  word_count: 25,
  created_at: "2024-02-15T10:00:00Z",
  updated_at: "2024-02-15T10:00:00Z",
  success_rate: 0.85,
  last_studied_at: "2024-02-14T15:30:00Z"
};

describe('GroupDetails', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading state initially', () => {
    (fetchGroupDetails as any).mockImplementation(() => new Promise(() => {}));
    
    renderWithClient(<GroupDetails groupId={1} /> as JSX.Element);
    
    expect(screen.getByTestId('skeleton-header')).toBeInTheDocument();
    expect(screen.getByTestId('skeleton-content')).toBeInTheDocument();
  });

  it('displays group data when loaded', async () => {
    (fetchGroupDetails as any).mockResolvedValue(mockGroup);
    
    renderWithClient(<GroupDetails groupId={1} /> as JSX.Element);
    
    await waitFor(() => {
      expect(screen.getByText('Common Verbs')).toBeInTheDocument();
      expect(screen.getByText('Words: 25')).toBeInTheDocument();
      expect(screen.getByText('Success Rate: 85.0%')).toBeInTheDocument();
    });
  });

  it('handles error state', async () => {
    const errorMessage = 'Failed to fetch group details';
    (fetchGroupDetails as any).mockRejectedValue(new Error(errorMessage));
    
    renderWithClient(<GroupDetails groupId={1} /> as JSX.Element);
    
    await waitFor(() => {
      expect(screen.getByText(`Error loading group details: ${errorMessage}`)).toBeInTheDocument();
    });
  });
});