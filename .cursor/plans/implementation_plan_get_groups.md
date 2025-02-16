# Implementation Plan: GET /groups Endpoint Integration

## Overview
This plan outlines the implementation of the groups listing endpoint and its frontend integration. The endpoint will provide paginated access to word groups with sorting capabilities.

## Prerequisites
- [x] Database table for groups exists
- [x] React Query setup in frontend
- [x] API client configuration
- [x] TypeScript environment

## Implementation Steps

### 1. Update API Types
- [x] Create Group interface in api.ts
- [x] Add GroupsResponse interface for pagination
- [x] Add fetchGroups function
```typescript:src/services/api.ts
export interface Group {
  id: number;
  name: string;
  word_count: number;
  created_at: string;
  updated_at: string;
}

export interface GroupsResponse {
  groups: Group[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export const fetchGroups = async (
  page: number = 1,
  per_page: number = 10,
  sort_by: string = 'name',
  order: 'asc' | 'desc' = 'asc'
): Promise<GroupsResponse> => {
  const response = await api.get('/groups', {
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

### 2. Create Groups Hook
- [x] Create useGroups.ts file
- [x] Implement hook with React Query
- [x] Add sorting and pagination support
```typescript:src/hooks/useGroups.ts
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { fetchGroups, type GroupsResponse } from '../services/api';

export interface UseGroupsParams {
  page: number;
  per_page: number;
  sort_by: string;
  order: 'asc' | 'desc';
}

export function useGroups(params: UseGroupsParams): UseQueryResult<GroupsResponse, Error> {
  return useQuery({
    queryKey: ['groups', params],
    queryFn: () => fetchGroups(
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

### 3. Create Groups List Component
- [x] 3.1. Create GroupsList component
- [x] 3.2. Add loading state with skeletons
- [x] 3.3. Implement error handling
- [x] 3.4. Add sorting controls
- [x] 3.5. Add pagination
```typescript:src/components/GroupsList.tsx
import { useState } from 'react';
import { useGroups } from '../hooks/useGroups';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Skeleton } from './ui/skeleton';
import { Pagination } from './ui/pagination';

export default function GroupsList() {
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState('name');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');
  
  const { data, isLoading, error } = useGroups({
    page,
    per_page: 10,
    sort_by: sortBy,
    order
  });

  // Component implementation...
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
```typescript:src/components/__tests__/GroupsList.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import GroupsList from '../GroupsList';

// Test implementation...
```

### 5. Update Navigation Context
- [x] 5.1. Add groups-related state
- [x] 5.2. Add setCurrentGroup action
- [x] 5.3. Update context types

## Testing Steps
- [x] 1. Start the development server
  ```bash
  npm run dev
  ```

- [x] 2. Navigate to groups page
  - Visit http://localhost:5173/groups
  - Verify the page loads without errors

- [x] 3. Verify loading state appears
  - Check that skeleton rows appear while data is loading
  - Verify correct number of skeleton rows (10)
  - Confirm skeleton styling matches design

- [x] 4. Verify groups list renders
  - Check that groups data appears after loading
  - Verify all columns display correctly:
    - Name
    - Word count
    - Created date
  - Confirm hover states work on rows
  - Verify table styling matches design

- [x] 5. Test sorting functionality
  - Click column headers to sort
  - Verify sort icons change appropriately
  - Confirm data reorders correctly
  - Test all sortable columns:
    - Name
    - Word count
    - Created date

- [x] 6. Test pagination
  - Verify page numbers display correctly
  - Test Previous/Next buttons
  - Confirm button disable states work
  - Check that data updates when changing pages

- [x] 7. Verify error handling
  - Test network error scenario
  - Verify error message displays
  - Confirm error styling matches design

- [x] 8. Run test suite
  ```bash
  npm run test
  ```
  - Verify all tests pass
  - Check test coverage

## API Documentation

### GET /groups

Fetch paginated list of word groups.

#### Request
- Method: `GET`
- URL: `/api/groups`
- Authentication: None (for now)

**Query Parameters:**
| Parameter | Type    | Required | Default | Description                                |
|-----------|---------|----------|---------|--------------------------------------------|
| page      | integer | No       | 1       | Page number                               |
| per_page  | integer | No       | 10      | Items per page (max 50)                  |
| sort_by   | string  | No       | 'name'  | Field to sort by (name/word_count/created_at) |
| order     | string  | No       | 'asc'   | Sort order (asc/desc)                    |

#### Response

**Success Response (200 OK)**
```json
{
  "groups": [
    {
      "id": 1,
      "name": "Common Verbs",
      "word_count": 25,
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

*Bad Request (400)*
```json
{
  "error": "Invalid page number"
}
```

*Server Error (500)*
```json
{
  "error": "Internal server error"
}
```

#### Notes
- Response is paginated with a maximum of 50 items per page
- Supports sorting by:
  - name (default)
  - word_count
  - created_at
- word_count is calculated from the related words
- Includes total count for pagination
- Timestamps are in ISO 8601 format
- All text fields are UTF-8 encoded

#### Rate Limiting
- Rate limit: 100 requests per minute per IP
- Rate limit headers included in response:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

#### Caching
- ETag support for caching
- Cache-Control: private, max-age=60
- Last-Modified header included 