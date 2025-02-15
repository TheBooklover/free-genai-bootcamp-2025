import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import WordShow from '../WordShow';
import { useNavigation } from '../../context/NavigationContext';
import type { ReactElement, JSXElementConstructor } from 'react';

// Mock the required modules
vi.mock('react-router-dom', () => ({
    useParams: vi.fn(),
    BrowserRouter: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock('@tanstack/react-query', () => ({
    useQuery: vi.fn(),
}));

vi.mock('../../context/NavigationContext', () => ({
    useNavigation: vi.fn(),
}));

// Mock data
const mockWord = {
    id: 1,
    quebecois: 'pogner',
    standard_french: 'attraper',
    english: 'to catch',
    pronunciation: 'pɔɲe',
    usage_notes: 'Common verb in Quebec',
    correct_count: 5,
    wrong_count: 2,
    groups: [
        { id: 1, name: 'Verbs' },
        { id: 2, name: 'Common Words' },
    ],
};

// Wrap component with router
const renderWithRouter = (component: ReactElement<any, JSXElementConstructor<any>>) => {
    return render(
        <BrowserRouter>
            {component}
        </BrowserRouter>
    );
};

describe('WordShow', () => {
    beforeEach(() => {
        vi.mocked(useNavigation).mockReturnValue({
            setCurrentWord: vi.fn(),
            currentWord: null,
        } as any);
    });

    it('renders loading state', () => {
        // Setup
        vi.mocked(useParams).mockReturnValue({ id: '1' });
        vi.mocked(useQuery).mockReturnValue({
            isLoading: true,
            data: undefined,
            error: null,
        } as any);

        // Render
        renderWithRouter(<WordShow />);

        // Assert
        expect(screen.getByTestId('loading-skeleton')).toBeInTheDocument();
    });

    it('renders word details when data is loaded', async () => {
        // Setup
        vi.mocked(useParams).mockReturnValue({ id: '1' });
        vi.mocked(useQuery).mockReturnValue({
            isLoading: false,
            data: mockWord,
            error: null,
        } as any);

        // Render
        renderWithRouter(<WordShow />);

        // Assert
        await waitFor(() => {
            expect(screen.getByText(mockWord.quebecois)).toBeInTheDocument();
            expect(screen.getByText(mockWord.standard_french)).toBeInTheDocument();
            expect(screen.getByText(mockWord.english)).toBeInTheDocument();
            expect(screen.getByText(mockWord.pronunciation)).toBeInTheDocument();
            expect(screen.getByText(mockWord.usage_notes)).toBeInTheDocument();
            expect(screen.getByText('Verbs')).toBeInTheDocument();
            expect(screen.getByText('Common Words')).toBeInTheDocument();
        });
    });

    it('renders error state', () => {
        // Setup
        vi.mocked(useParams).mockReturnValue({ id: '1' });
        vi.mocked(useQuery).mockReturnValue({
            isLoading: false,
            data: undefined,
            error: new Error('Failed to fetch word'),
        } as any);

        // Render
        renderWithRouter(<WordShow />);

        // Assert
        expect(screen.getByText('Error: Failed to fetch word')).toBeInTheDocument();
    });

    it('renders not found state when no word is returned', () => {
        // Setup
        vi.mocked(useParams).mockReturnValue({ id: '1' });
        vi.mocked(useQuery).mockReturnValue({
            isLoading: false,
            data: undefined,
            error: null,
        } as any);

        // Render
        renderWithRouter(<WordShow />);

        // Assert
        expect(screen.getByText('Word not found')).toBeInTheDocument();
    });
}); 