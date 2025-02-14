# Implementation Plan: POST /study_sessions/<id>/review Route

## Overview
This plan outlines the steps to implement an endpoint for submitting word reviews during a study session. Users can submit whether they got words correct or incorrect during their review session.

## Prerequisites
- [x] Existing study_sessions table
- [x] Existing word_review_items table
- [x] Study session creation endpoint

## Implementation Steps

### 1. Route Setup
- [x] Implement basic route handler

### 2. Request Validation
- [x] Implement validation function
- [x] Add validation to route handler

### 3. Session Verification
- [x] Add session existence check

### 4. Word Verification
- [x] Add word existence check

### 5. Database Operations
- [x] Implement review insertion

### 6. Response Creation
- [x] Implement response data query
- [x] Format response data

### 7. Error Handling
- [x] Add try-catch block
- [x] Implement database rollback

## Testing Plan

### Unit Tests
- [x] Implement success test
- [x] Implement invalid session test
- [x] Implement invalid word test
- [x] Implement invalid data test
```python
def test_submit_review_success():
    response = client.post('/api/study-sessions/1/review', json={
        'word_id': 1,
        'correct': True
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['word_id'] == 1
    assert data['correct'] == True

def test_submit_review_invalid_session():
    response = client.post('/api/study-sessions/999/review', json={
        'word_id': 1,
        'correct': True
    })
    assert response.status_code == 404

def test_submit_review_invalid_word():
    response = client.post('/api/study-sessions/1/review', json={
        'word_id': 999,
        'correct': True
    })
    assert response.status_code == 404

def test_submit_review_invalid_data():
    response = client.post('/api/study-sessions/1/review', json={
        'word_id': 1
        # missing correct field
    })
    assert response.status_code == 400
```

## API Documentation
- [x] Document request format
- [x] Document success response
- [x] Document error responses

### POST /api/study-sessions/{session_id}/review

Submit a word review for a study session.

#### Request
- Method: `POST`
- URL: `/api/study-sessions/{session_id}/review`
- Rate limit: 20 requests per minute

**URL Parameters:**
- `session_id` (integer, required): ID of the study session

**Request Body:**
```json
{
    "word_id": 1,        // Integer, required: ID of the word being reviewed
    "correct": true      // Boolean, required: Whether the word was reviewed correctly
}
```

#### Responses

**Success Response (200 OK)**
```json
{
    "id": 1,                            // Integer: Review item ID
    "word_id": 1,                       // Integer: Word ID
    "kanji": "漢字",                    // String: Word's kanji
    "romaji": "kanji",                  // String: Word's romaji
    "english": "chinese characters",     // String: Word's English translation
    "correct": true,                    // Boolean: Review result
    "reviewed_at": "2024-02-09T12:00:00" // String: ISO 8601 timestamp
}
```

**Error Responses**

*Bad Request (400)*
```json
{
    "error": "Missing word_id"          // When word_id is missing
}
```
```json
{
    "error": "Missing correct field"    // When correct field is missing
}
```
```json
{
    "error": "correct field must be a boolean"  // When correct is not boolean
}
```
```json
{
    "error": "word_id must be an integer"      // When word_id is not integer
}
```

*Not Found (404)*
```json
{
    "error": "Study session not found"  // When session_id doesn't exist
}
```
```json
{
    "error": "Word not found"           // When word_id doesn't exist
}
```

*Rate Limit Exceeded (429)*
```json
{
    "error": "Too many requests",
    "message": "Please try again later",
    "retry_after": "Wait 30 seconds"
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
curl -X POST \
  http://api.example.com/api/study-sessions/123/review \
  -H 'Content-Type: application/json' \
  -d '{
    "word_id": 456,
    "correct": true
  }'
```

## Additional Considerations
- [ ] Add logging for debugging and monitoring
- [ ] Consider adding batch review submission
- [ ] Add validation for duplicate reviews
- [ ] Consider adding review modification endpoint
- [ ] Add statistics calculation for session performance