# Implementation Plan: POST /study_sessions/<id>/review Route

## Overview
This plan outlines the steps to implement an endpoint for submitting word reviews during a study session. Users can submit whether they got words correct or incorrect during their review session.

## Prerequisites
- [x] Existing study_sessions table
- [x] Existing word_review_items table
- [x] Study session creation endpoint

## Implementation Steps

### 1. Route Setup
```python
@app.route('/api/study-sessions/<int:session_id>/review', methods=['POST'])
@cross_origin()
@limiter.limit("20 per minute")
def submit_session_review(session_id):
    pass
```

### 2. Request Validation
```python
def validate_review_request(data):
    if 'word_id' not in data:
        return False, "Missing word_id"
    if 'correct' not in data:
        return False, "Missing correct field"
    if not isinstance(data['correct'], bool):
        return False, "correct field must be a boolean"
    return True, None

# In route handler:
data = request.get_json()
is_valid, error_message = validate_review_request(data)
if not is_valid:
    return jsonify({"error": error_message}), 400
```

### 3. Session Verification
```python
cursor.execute('''
    SELECT EXISTS(SELECT 1 FROM study_sessions WHERE id = ?) as session_exists
''', (session_id,))

if not cursor.fetchone()['session_exists']:
    return jsonify({"error": "Study session not found"}), 404
```

### 4. Word Verification
```python
cursor.execute('''
    SELECT EXISTS(SELECT 1 FROM words WHERE id = ?) as word_exists
''', (data['word_id'],))

if not cursor.fetchone()['word_exists']:
    return jsonify({"error": "Word not found"}), 404
```

### 5. Database Operations
```python
cursor.execute('''
    INSERT INTO word_review_items (
        study_session_id,
        word_id,
        correct,
        reviewed_at
    ) VALUES (?, ?, ?, ?)
''', (session_id, data['word_id'], data['correct'], datetime.now()))

review_id = cursor.lastrowid
```

### 6. Response Creation
```python
cursor.execute('''
    SELECT 
        wri.id,
        wri.word_id,
        w.kanji,
        w.romaji,
        w.english,
        wri.correct,
        wri.reviewed_at
    FROM word_review_items wri
    JOIN words w ON w.id = wri.word_id
    WHERE wri.id = ?
''', (review_id,))

review = cursor.fetchone()
```

### 7. Error Handling
```python
try:
    cursor = app.db.cursor()
    # ... implementation ...
    app.db.commit()
except Exception as e:
    app.db.rollback()
    return jsonify({"error": str(e)}), 500
```

## Testing Plan

### Unit Tests
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

### POST /api/study-sessions/<id>/review

Submit a word review for a study session.

**Request Body:**
```json
{
    "word_id": 1,
    "correct": true
}
```

**Success Response:**
```json
{
    "id": 1,
    "word_id": 1,
    "kanji": "漢字",
    "romaji": "kanji",
    "english": "chinese characters",
    "correct": true,
    "reviewed_at": "2024-02-09T12:00:00"
}
```

**Error Response:**
```json
{
    "error": "Error message here"
}
```

## Additional Considerations
- [ ] Add logging for debugging and monitoring
- [ ] Consider adding batch review submission
- [ ] Add validation for duplicate reviews
- [ ] Consider adding review modification endpoint
- [ ] Add statistics calculation for session performance 