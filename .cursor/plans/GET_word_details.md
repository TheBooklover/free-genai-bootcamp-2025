# Implementation Plan: GET /words/{wordId} Route

## Overview
This plan outlines the implementation of an endpoint for fetching detailed information about a specific word, including its groups and review statistics.

## Prerequisites
- [x] Existing words table
- [x] Existing word_groups table
- [x] Existing groups table
- [x] Existing word_reviews table

## Implementation Steps

### 1. Route Setup
- [x] Create route handler in words.py
```python
@words_bp.route('/<int:word_id>', methods=['GET'])
@cross_origin()
def get_word_details(word_id):
    pass
```

### 2. Database Query
- [x] Write base word query
```python
cursor.execute('''
    SELECT w.id, w.quebecois, w.standard_french, w.english,
           w.pronunciation, w.usage_notes,
           COALESCE(r.correct_count, 0) AS correct_count,
           COALESCE(r.wrong_count, 0) AS wrong_count
    FROM words w
    LEFT JOIN word_reviews r ON w.id = r.word_id
    WHERE w.id = ?
''', (word_id,))
```

### 3. Groups Query
- [x] Add query for word's groups
```python
# Groups are included in the main query using JOINs and GROUP_CONCAT
cursor.execute('''
    SELECT w.id, w.quebecois, w.standard_french, w.english,
           w.pronunciation, w.usage_notes,
           COALESCE(r.correct_count, 0) AS correct_count,
           COALESCE(r.wrong_count, 0) AS wrong_count,
           GROUP_CONCAT(DISTINCT g.id || '::' || g.name) as groups
    FROM words w
    LEFT JOIN word_reviews r ON w.id = r.word_id
    LEFT JOIN word_groups wg ON w.id = wg.word_id
    LEFT JOIN groups g ON wg.group_id = g.id
    WHERE w.id = ?
    GROUP BY w.id
''', (word_id,))
```

### 4. Response Formatting
- [x] Format word details
- [x] Format groups list
- [x] Combine into response object
```python
# Parse groups from GROUP_CONCAT result
groups = []
if word["groups"]:
    groups = [
        {"id": int(group_id), "name": group_name}
        for group_str in word["groups"].split(',')
        for group_id, group_name in [group_str.split('::')]
    ]

# Format and return response
return jsonify({
    "word": {
        "id": word["id"],
        "quebecois": word["quebecois"],
        "standard_french": word["standard_french"],
        "english": word["english"],
        "pronunciation": word["pronunciation"],
        "usage_notes": word["usage_notes"],
        "correct_count": word["correct_count"],
        "wrong_count": word["wrong_count"],
        "groups": groups
    }
})
```

### 5. Error Handling
- [x] Add word existence check
- [x] Add try-catch block
```python
try:
    cursor = g.db.cursor()
    
    # ... query execution ...
    
    word = cursor.fetchone()
    
    if not word:
        return jsonify({"error": "Word not found"}), 404
        
    # ... response formatting ...
    
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

### 6. Testing
- [x] Create test file
- [x] Add test cases

```python
def test_get_word_by_id(client):
    """Test getting a single word by ID"""
    # First get a list of words to get a valid ID
    response = client.get('/api/words')
    data = json.loads(response.data)
    
    if len(data['words']) > 0:
        word_id = data['words'][0]['id']
        
        # Test getting the specific word
        response = client.get(f'/api/words/{word_id}')
        assert response.status_code == 200
        word_data = json.loads(response.data)
        assert 'word' in word_data
        assert word_data['word']['id'] == word_id
```

## API Documentation

### GET /words/{word_id}

Fetch detailed information about a specific word.

#### Request
- Method: `GET`
- URL: `/api/words/{word_id}`

**URL Parameters:**
- `word_id` (integer, required): ID of the word to fetch

#### Responses

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

*Bad Request (400)*
```json
{
    "error": "Invalid word ID format"
}
```

*Not Found (404)*
```json
{
    "error": "Word not found"
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
curl -X GET http://localhost:5000/api/words/123
```

## Additional Considerations
- [ ] Add caching for frequently accessed words
- [ ] Add request rate limiting
- [ ] Add logging for monitoring
- [ ] Consider adding more word metadata (created_at, updated_at)
- [ ] Consider adding study history for the word