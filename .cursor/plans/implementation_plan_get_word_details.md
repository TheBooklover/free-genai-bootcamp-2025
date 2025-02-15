# Implementation Plan: GET /words/{wordId} Endpoint Integration

## Overview
This plan outlines how to implement and integrate the word details endpoint with the React frontend, ensuring proper data fetching and display.

## Prerequisites
- [x] Backend route for GET /words/{wordId} implemented
- [x] React Query setup in frontend
- [x] TypeScript types for Word interface
- [x] API client configuration

## Implementation Steps

### 1. Update API Types
```typescript:src/services/api.ts
// Add or update Word interface
export interface Word {
  id: number;
  quebecois: string;
  standard_french: string;
  english: string;
  pronunciation?: string;
  usage_notes?: string;
  correct_count: number;
  wrong_count: number;
  groups?: Array<{
    id: number;
    name: string;
  }>;
}

// Add fetch function
export const fetchWordDetails = async (wordId: string | number): Promise<Word> => {
  const response = await api.get(`/words/${wordId}`);
  return response.data.word;
};
```

### 2. Create Word Details Hook
```typescript:src/hooks/useWordDetails.ts
import { useQuery } from '@tanstack/react-query';
import { fetchWordDetails, type Word } from '@/services/api';

export function useWordDetails(wordId: string | number) {
  return useQuery({
    queryKey: ['word', wordId],
    queryFn: () => fetchWordDetails(wordId),
    enabled: !!wordId,
  });
}
```

### 3. Update WordShow Component
```typescript:src/pages/WordShow.tsx
import { useParams } from 'react-router-dom';
import { useWordDetails } from '@/hooks/useWordDetails';
import { useNavigation } from '@/context/NavigationContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function WordShow() {
  const { id } = useParams<{ id: string }>();
  const { data: word, isLoading, error } = useWordDetails(id!);
  const { setCurrentWord } = useNavigation();

  useEffect(() => {
    if (word) {
      setCurrentWord(word);
    }
  }, [word, setCurrentWord]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!word) {
    return <div>Word not found</div>;
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{word.quebecois}</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="grid grid-cols-2 gap-4">
            <div>
              <dt className="text-sm font-medium text-gray-500">Standard French</dt>
              <dd className="text-lg">{word.standard_french}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">English</dt>
              <dd className="text-lg">{word.english}</dd>
            </div>
            {word.pronunciation && (
              <div>
                <dt className="text-sm font-medium text-gray-500">Pronunciation</dt>
                <dd className="text-lg">{word.pronunciation}</dd>
              </div>
            )}
            {word.usage_notes && (
              <div className="col-span-2">
                <dt className="text-sm font-medium text-gray-500">Usage Notes</dt>
                <dd className="text-lg">{word.usage_notes}</dd>
              </div>
            )}
          </dl>
        </CardContent>
      </Card>
      
      {word.groups && word.groups.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Groups</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2 flex-wrap">
              {word.groups.map(group => (
                <span 
                  key={group.id}
                  className="px-2 py-1 bg-primary/10 rounded-md text-sm"
                >
                  {group.name}
                </span>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
```

### 4. Add Tests
```typescript:src/pages/__tests__/WordShow.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import WordShow from '../WordShow';

// Mock dependencies
vi.mock('react-router-dom', () => ({
  useParams: vi.fn(),
}));

vi.mock('@tanstack/react-query', () => ({
  useQuery: vi.fn(),
}));

vi.mock('@/context/NavigationContext', () => ({
  useNavigation: () => ({
    setCurrentWord: vi.fn(),
  }),
}));

describe('WordShow', () => {
  it('renders loading state', () => {
    vi.mocked(useParams).mockReturnValue({ id: '1' });
    vi.mocked(useQuery).mockReturnValue({
      isLoading: true,
      data: undefined,
      error: null,
    } as any);

    render(<WordShow />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders word details', async () => {
    const mockWord = {
      id: 1,
      quebecois: 'pogner',
      standard_french: 'attraper',
      english: 'to catch',
      pronunciation: 'pɔɲe',
      usage_notes: 'Common verb',
      groups: [{ id: 1, name: 'Verbs' }],
    };

    vi.mocked(useParams).mockReturnValue({ id: '1' });
    vi.mocked(useQuery).mockReturnValue({
      isLoading: false,
      data: mockWord,
      error: null,
    } as any);

    render(<WordShow />);
    
    await waitFor(() => {
      expect(screen.getByText('pogner')).toBeInTheDocument();
      expect(screen.getByText('attraper')).toBeInTheDocument();
      expect(screen.getByText('to catch')).toBeInTheDocument();
      expect(screen.getByText('Common verb')).toBeInTheDocument();
      expect(screen.getByText('Verbs')).toBeInTheDocument();
    });
  });

  it('renders error state', () => {
    vi.mocked(useParams).mockReturnValue({ id: '1' });
    vi.mocked(useQuery).mockReturnValue({
      isLoading: false,
      data: undefined,
      error: new Error('Failed to fetch'),
    } as any);

    render(<WordShow />);
    expect(screen.getByText('Error: Failed to fetch')).toBeInTheDocument();
  });
});
```

### 5. Update Navigation Context
```typescript:src/context/NavigationContext.tsx
// Add or update Word type import
import type { Word } from '@/services/api';

interface NavigationContextType {
  currentWord: Word | null;
  setCurrentWord: (word: Word | null) => void;
  // ... other context properties
}
```

## Testing Steps
1. Start the development server
2. Navigate to a word detail page (e.g., /words/1)
3. Verify loading state appears
4. Verify word details render correctly
5. Verify groups are displayed if present
6. Verify error handling works by temporarily breaking the API URL
7. Run the test suite: `npm run test`

## Additional Considerations
- [ ] Add error boundary for component-level error handling
- [ ] Implement loading skeletons for better UX
- [ ] Add retry logic for failed requests
- [ ] Consider adding word detail caching strategy
- [ ] Add proper TypeScript types for API responses 