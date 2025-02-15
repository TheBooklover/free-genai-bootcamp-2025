import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@/test/utils';
import WordShow from '../WordShow';
import { useParams } from 'react-router-dom';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { useNavigation } from '@/context/NavigationContext';
import type { Word } from '../WordShow';

// Mock NavigationContext
vi.mock('@/context/NavigationContext', () => ({
    useNavigation: () => ({
        setCurrentWord: vi.fn(),
    }),
}));

// Mock react-router-dom
vi.mock('react-router-dom', () => ({
    useParams: vi.fn(),
    Link: vi.fn(() => null),
}));

// Mock react-query
vi.mock('@tanstack/react-query', () => ({
    useQuery: vi.fn(),
}));

describe('WordShow', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(useParams).mockReturnValue({ wordId: '1' });
    });

    it('renders word details', async () => {
        vi.mocked(useQuery).mockReturnValue({
            data: {
                id: 1,
                quebecois: "char",
                standard_french: "voiture",
                english: "car",
                correct_count: 0,
                wrong_count: 0,
            },
            isLoading: false,
            error: null,
            status: 'success',
            isError: false,
            isPending: false,
            isSuccess: true,
            refetch: vi.fn(),
        } as UseQueryResult<Word, Error>);

        render(<WordShow />);
        expect(await screen.findByText('char')).toBeInTheDocument();
    });

    it('displays loading state', async () => {
        vi.mocked(useQuery).mockReturnValue({
            data: null,
            isLoading: true,
            error: null,
        });

        render(<WordShow />);
        expect(await screen.findByText(/loading/i)).toBeInTheDocument();
    });

    it('handles error state', async () => {
        vi.mocked(useQuery).mockReturnValue({
            data: null,
            isLoading: false,
            error: new Error('Failed to fetch'),
        });

        render(<WordShow />);
        expect(await screen.findByText('Failed to load word details')).toBeInTheDocument();
    });
}); 