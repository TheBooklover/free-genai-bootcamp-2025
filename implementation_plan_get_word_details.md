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
- [x] Add or update Word interface in api.ts
- [x] Add fetchWordDetails function
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
- [x] Create useWordDetails.ts file
- [x] Implement hook with React Query
- [x] Add proper type definitions
  - [x] Add UseQueryResult type
  - [x] Add explicit return type
  - [x] Fix import paths
```typescript:src/hooks/useWordDetails.ts
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { fetchWordDetails, type Word } from '../services/api';

export function useWordDetails(wordId: string | number): UseQueryResult<Word, Error> {
  return useQuery({
    queryKey: ['word', wordId],
    queryFn: () => fetchWordDetails(wordId),
    enabled: !!wordId,
  });
}
```

### 3. Update WordShow Component
- [x] 3.1. Add imports and type definitions
- [x] 3.2. Implement loading state with skeleton
- [x] 3.3. Add error handling
- [x] 3.4. Create word details display
- [x] 3.5. Add groups display section

### 4. Add Tests
- [x] 4.1. Create test file if not exists
- [x] 4.2. Add mock setup for dependencies
- [x] 4.3. Implement loading state test
- [x] 4.4. Implement successful render test
- [x] 4.5. Implement error state test

### 5. Update Navigation Context
- [x] 5.1. Import Word type
- [x] 5.2. Update context interface
- [x] 5.3. Add currentWord state
- [x] 5.4. Implement setCurrentWord function

## Testing Steps
- [x] 1. Install required testing dependencies
- [x] 2. Set up test environment
- [x] 3. Run the test suite
- [x] 4. Verify all tests pass
  - [x] Loading state test passed
  - [x] Word details render test passed
  - [x] Error state test passed
  - [x] Not found state test passed
- [ ] 5. Check test coverage

## API Documentation

### GET /words/{wordId}

Fetch detailed information about a specific word.

#### Request
- Method: `GET`
- URL: `/api/words/{wordId}`
- Authentication: None (for now)

**URL Parameters:**
| Parameter | Type    | Required | Description        |
|-----------|---------|----------|--------------------|
| wordId    | integer | Yes      | ID of word to fetch|

#### Response

**Success Response (200 OK)**
```json
{
  "word": {
    "id": 1,
    "quebecois": "pogner",
    "standard_french": "attraper",
    "english": "to catch/grab",
    "pronunciation": "pɔɲe",
    "usage_notes": "Very versatile verb in Quebec. Can mean to catch, grab, get, or understand.",
    "correct_count": 5,
    "wrong_count": 2,
    "groups": [
      {
        "id": 1,
        "name": "Common Verbs"
      },
      {
        "id": 2,
        "name": "Everyday Speech"
      }
    ]
  }
}
```

**Error Responses**

*Not Found (404)*
```json
{
  "error": "Word not found"
}
```

*Bad Request (400)*
```json
{
  "error": "Invalid word ID format"
}
```

*Server Error (500)*
```json
{
  "error": "Internal server error message"
}
```

#### Example Usage

```bash
# Fetch word with ID 123
curl -X GET http://localhost:5000/api/words/123

# Using axios in TypeScript
const response = await api.get(`/words/${wordId}`);
const word = response.data.word;
```

#### Notes
- The endpoint includes groups the word belongs to
- Correct and wrong counts reflect the study history
- Optional fields (pronunciation, usage_notes) may be null
- Groups array may be empty

#### Rate Limiting
- Current limit: None
- Future consideration: Implement rate limiting for production

#### Caching
- Current: No caching
- Future consideration: Add ETag support for caching