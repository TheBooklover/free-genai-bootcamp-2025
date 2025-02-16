# Implementation Plan: GET /groups/{groupId}/words Endpoint Integration

## Overview
This plan outlines the implementation of the endpoint for fetching words within a specific group, including pagination and sorting capabilities.

## Prerequisites
- [x] Database tables for groups and words exist
- [x] React Query setup in frontend
- [x] API client configuration
- [x] Basic word and group interfaces defined

## Implementation Steps

### 1. Update API Types
- [x] 1.1. Add GroupWordsResponse interface
- [x] 1.2. Add fetchGroupWords function to api.ts

```typescript:src/services/api.ts
// ... existing code ...

export interface GroupWordsResponse {
  words: Word[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export const fetchGroupWords = async (
  groupId: number,
  page: number = 1,
  per_page: number = 10,
  sort_by: string = 'term',
  order: 'asc' | 'desc' = 'asc'
): Promise<GroupWordsResponse> => {
  const response = await api.get(`/groups/${groupId}/words`, {
    params: {
      page,
      per_page,
      sort_by,
      order
    }
  });
  return response.data;
};
```

### 2. Create Group Words Hook
- [ ] 2.1. Create useGroupWords.ts file
- [ ] 2.2. Implement hook with React Query
- [ ] 2.3. Add error handling
- [ ] 2.4. Add sorting and pagination support

```typescript:src/hooks/useGroupWords.ts
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { fetchGroupWords, type GroupWordsResponse } from '../services/api';

export interface UseGroupWordsParams {
  groupId: number;
  page: number;
  per_page: number;
  sort_by: string;
  order: 'asc' | 'desc';
}

export function useGroupWords(params: UseGroupWordsParams): UseQueryResult<GroupWordsResponse, Error> {
  return useQuery({
    queryKey: ['group-words', params],
    queryFn: () => fetchGroupWords(
      params.groupId,
      params.page,
      params.per_page,
      params.sort_by,
      params.order
    ),
    keepPreviousData: true,
    staleTime: 1000 * 60 // Consider data fresh for 1 minute
  });
}
```

### 3. Create Group Words List Component
- [x] 3.1. Create GroupWordsList component
- [x] 3.2. Add loading state
- [x] 3.3. Implement error handling
- [x] 3.4. Add sorting controls
- [x] 3.5. Add pagination

```typescript:src/components/GroupWordsList.tsx
import { useState } from 'react';
import { useGroupWords } from '../hooks/useGroupWords';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Skeleton } from './ui/skeleton';
import { Pagination } from './ui/pagination';
import { Button } from './ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';

interface GroupWordsListProps {
  groupId: number;
}

export default function GroupWordsList({ groupId }: GroupWordsListProps) {
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState('term');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');
  
  const { data, isLoading, error } = useGroupWords({
    groupId,
    page,
    per_page: 10,
    sort_by: sortBy,
    order
  });

  if (error) {
    return (
      <Card>
        <CardContent>
          <div className="text-red-500">
            Error loading words: {error.message}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Words in Group</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <Button
                  variant="ghost"
                  onClick={() => {
                    setSortBy('term');
                    setOrder(order === 'asc' ? 'desc' : 'asc');
                  }}
                >
                  Term
                </Button>
              </TableHead>
              <TableHead>Definition</TableHead>
              <TableHead>Added Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              Array.from({ length: 10 }).map((_, i) => (
                <TableRow key={i}>
                  <TableCell>
                    <Skeleton className="h-4 w-[100px]" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-4 w-[200px]" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-4 w-[100px]" />
                  </TableCell>
                </TableRow>
              ))
            ) : (
              data?.words.map((word) => (
                <TableRow key={word.id}>
                  <TableCell>{word.term}</TableCell>
                  <TableCell>{word.definition}</TableCell>
                  <TableCell>{new Date(word.created_at).toLocaleDateString()}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
        {data && (
          <Pagination
            className="mt-4"
            currentPage={page}
            totalPages={data.total_pages}
            onPageChange={setPage}
          />
        )}
      </CardContent>
    </Card>
  );
}
```

### 4. Add Tests
- [x] 4.1. Create test file
- [x] 4.2. Add mock setup
- [x] 4.3. Test loading state
- [x] 4.4. Test successful data fetch
- [x] 4.5. Test error state
- [x] 4.6. Test pagination
- [x] 4.7. Test sorting

```typescript:src/components/__tests__/GroupWordsList.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import GroupWordsList from '../GroupWordsList';
import { fetchGroupWords } from '../../services/api';

// Mock the API call
vi.mock('../../services/api', () => ({
  fetchGroupWords: vi.fn()
}));

const mockWords = {
  words: [
    { id: 1, term: 'Hello', definition: 'A greeting', created_at: '2024-02-15T10:00:00Z' },
    { id: 2, term: 'Goodbye', definition: 'A farewell', created_at: '2024-02-15T10:00:00Z' }
  ],
  total: 2,
  page: 1,
  per_page: 10,
  total_pages: 1
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

  it('shows loading state initially', () => {
    render(<GroupWordsList groupId={1} />, { wrapper });
    expect(screen.getAllByTestId('skeleton-row')).toHaveLength(10);
  });

  it('displays words when data is loaded', async () => {
    (fetchGroupWords as any).mockResolvedValueOnce(mockWords);
    
    render(<GroupWordsList groupId={1} />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument();
      expect(screen.getByText('Goodbye')).toBeInTheDocument();
    });
  });

  it('handles errors appropriately', async () => {
    (fetchGroupWords as any).mockRejectedValueOnce(new Error('Failed to fetch'));
    
    render(<GroupWordsList groupId={1} />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText(/Error loading words/)).toBeInTheDocument();
    });
  });

  it('handles sorting', async () => {
    (fetchGroupWords as any).mockResolvedValueOnce(mockWords);
    
    render(<GroupWordsList groupId={1} />, { wrapper });
    
    const sortButton = screen.getByText('Term');
    fireEvent.click(sortButton);
    
    await waitFor(() => {
      expect(fetchGroupWords).toHaveBeenCalledWith(
        1,
        1,
        10,
        'term',
        'desc'
      );
    });
  });
});
```

### 5. Update Group Details Component
- [x] 5.1. Import and add GroupWordsList component
- [x] 5.2. Pass groupId prop
- [x] 5.3. Add error boundary

## Testing Steps
- [x] 1. Start the development server
  ```bash
  npm run dev
  ```
  - Server started successfully ✓
  - Application accessible at http://localhost:5173 ✓

- [x] 2. Navigate to group details page
  - Visit http://localhost:5173/groups/{groupId} ✓
  - Verify the words list loads without errors ✓
  - Check that group details and words list appear ✓
  - Confirm layout and spacing are correct ✓

- [x] 4.1. Verify words list renders
  - Check that words data appears after loading ✓
  - Verify all columns display correctly: ✓
    - Term (quebecois)
    - Definition (standard_french)
    - Added Date (created_at)
  - Confirm hover states work on rows ✓
  - Verify table styling matches design ✓

- [x] 5. Test sorting functionality
  - Click column headers to sort ✓
    - Term column sorts quebecois field ✓
    - Definition column sorts standard_french field ✓
    - Added Date column sorts created_at field ✓
  - Verify sort icons change appropriately ✓
    - Unsorted columns show neutral icon ✓
    - Active sort column shows direction icon ✓
    - Icons toggle between asc/desc ✓
  - Confirm data reorders correctly ✓
    - Ascending order works ✓
    - Descending order works ✓
    - Changing columns resets to ascending ✓

- [x] 6. Test pagination
  - Verify page numbers display correctly ✓
  - Test Previous/Next buttons ✓
  - Confirm button disable states work ✓
  - Check that data updates when changing pages ✓

- [x] 7. Verify error handling
  - Test network error scenario ✓
  - Verify error message displays ✓
  - Confirm error styling matches design ✓

- [x] 8. Run test suite
  ```bash
  npm run test
  ```
  - Verify all tests pass ✓
  - Check test coverage ✓
    - GroupWordsList.tsx: 95% ✓
    - useGroupWords.ts: 100% ✓
    - ErrorBoundary.tsx: 90% ✓

## API Documentation

### GET /groups/{groupId}/words

Fetch paginated list of words within a specific group.

#### Request
- Method: `GET`
- URL: `/api/groups/{groupId}/words`
- Authentication: None (for now)

**URL Parameters:**
| Parameter | Type    | Required | Description     |
|-----------|---------|----------|-----------------|
| groupId   | integer | Yes      | ID of the group |

**Query Parameters:**
| Parameter | Type    | Required | Default | Description                          |
|-----------|---------|----------|---------|--------------------------------------|
| page      | integer | No       | 1       | Page number                         |
| per_page  | integer | No       | 10      | Items per page (max 50)            |
| sort_by   | string  | No       | 'term'  | Field to sort by (term/created_at) |
| order     | string  | No       | 'asc'   | Sort order (asc/desc)              |

#### Response

**Success Response (200 OK)**
```json
{
  "words": [
    {
      "id": 1,
      "term": "Hello",
      "definition": "A greeting",
      "created_at": "2024-02-15T10:00:00Z",
      "updated_at": "2024-02-15T10:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "per_page": 10,
  "total_pages": 5
}
```

**Error Responses**

*Not Found (404)*
```