# Implementation Plan: POST /study_sessions Route

## Overview
This plan outlines the steps to implement a new POST endpoint for creating study sessions. The implementation will follow the existing patterns seen in the codebase and include validation, database operations, and error handling.

## Prerequisites
- [x] Review the existing study sessions routes and database schema
- [x] Ensure you have a local development environment set up
- [x] Verify database access and permissions

## Implementation Steps

### 1. Route Setup
- [x] Add the new route decorator:
```python
@app.route('/api/study-sessions', methods=['POST'])
@cross_origin()
def create_study_session():
    pass
```

### 2. Request Validation
- [x] Add validation for required fields:
```python
def validate_study_session_request(data):
    required_fields = ['group_id', 'study_activity_id']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, None

# In the route handler:
data = request.get_json()
is_valid, error_message = validate_study_session_request(data)
if not is_valid:
    return jsonify({"error": error_message}), 400
```

### 3. Database Operations
- [x] Create the SQL insert statement:
```python
cursor.execute('''
    INSERT INTO study_sessions (group_id, study_activity_id, created_at)
    VALUES (?, ?, ?)
''', (data['group_id'], data['study_activity_id'], datetime.now()))

session_id = cursor.lastrowid
```

### 4. Response Creation
- [x] Fetch the created session details:
```python
cursor.execute('''
    SELECT 
        ss.id,
        ss.group_id,
        g.name as group_name,
        sa.id as activity_id,
        sa.name as activity_name,
        ss.created_at
    FROM study_sessions ss
    JOIN groups g ON g.id = ss.group_id
    JOIN study_activities sa ON sa.id = ss.study_activity_id
    WHERE ss.id = ?
''', (session_id,))

session = cursor.fetchone()
```

### 5. Error Handling
- [x] Add try-catch block and database transaction:
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
- [x] Test successful creation:
```python
def test_create_study_session_success():
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 1
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert data['group_id'] == 1
    assert data['study_activity_id'] == 1
```

- [x] Test missing required fields:
```python
def test_create_study_session_missing_fields():
    response = client.post('/api/study-sessions', json={
        'group_id': 1
        # missing study_activity_id
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
```

- [x] Test invalid group_id:
```python
def test_create_study_session_invalid_group():
    response = client.post('/api/study-sessions', json={
        'group_id': 999999,  # non-existent group
        'study_activity_id': 1
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
```

## Complete Implementation

Here's the complete implementation to aim for:

```python
@app.route('/api/study-sessions', methods=['POST'])
@cross_origin()
def create_study_session():
    try:
        cursor = app.db.cursor()
        
        # Validate request data
        data = request.get_json()
        is_valid, error_message = validate_study_session_request(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400
            
        # Verify group and activity exist
        cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?) as group_exists,
                   EXISTS(SELECT 1 FROM study_activities WHERE id = ?) as activity_exists
        ''', (data['group_id'], data['study_activity_id']))
        
        result = cursor.fetchone()
        if not result['group_exists']:
            return jsonify({"error": "Group not found"}), 400
        if not result['activity_exists']:
            return jsonify({"error": "Study activity not found"}), 400
        
        # Create study session
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (?, ?, ?)
        ''', (data['group_id'], data['study_activity_id'], datetime.now()))
        
        session_id = cursor.lastrowid
        
        # Fetch created session
        cursor.execute('''
            SELECT 
                ss.id,
                ss.group_id,
                g.name as group_name,
                sa.id as activity_id,
                sa.name as activity_name,
                ss.created_at
            FROM study_sessions ss
            JOIN groups g ON g.id = ss.group_id
            JOIN study_activities sa ON sa.id = ss.study_activity_id
            WHERE ss.id = ?
        ''', (session_id,))
        
        session = cursor.fetchone()
        
        app.db.commit()
        
        return jsonify({
            'id': session['id'],
            'group_id': session['group_id'],
            'group_name': session['group_name'],
            'activity_id': session['activity_id'],
            'activity_name': session['activity_name'],
            'start_time': session['created_at'],
            'end_time': session['created_at'],  # For now, just use the same time
            'review_items_count': 0  # New session has no review items yet
        })
        
    except Exception as e:
        app.db.rollback()
        return jsonify({"error": str(e)}), 500
```

## Additional Considerations
- [x] Add logging for debugging and monitoring
  - Added app.logger.info/debug/warning/error calls throughout
  - Logging key events like session creation, errors, and validations
- [x] Add request rate limiting
  - Added Flask-Limiter with 20 requests per minute limit
  - Added custom error handler for rate limit exceeded
  - Added default limits of 200/day and 50/hour
- [x] Add input sanitization for security
  - Added ID conversion to integers
  - Added validation of ID formats
  - Added proper error messages for invalid inputs
- [x] Document the API endpoint
  - Added detailed comments throughout the code
  - Documented response format and error cases
  - Included example responses in documentation
- [x] Add integration tests
  - Added test fixtures in conftest.py
  - Added success case test
  - Added error case tests
  - Added input validation tests

## Documentation for API Endpoint

### POST /api/study-sessions

Creates a new study session.

**Request Body:**
```json
{
    "group_id": 1,
    "study_activity_id": 1
}
```

**Success Response:**
```json
{
    "id": 1,
    "group_id": 1,
    "group_name": "Example Group",
    "activity_id": 1,
    "activity_name": "Example Activity",
    "start_time": "2024-02-09T12:00:00",
    "end_time": "2024-02-09T12:00:00",
    "review_items_count": 0
}
```

**Error Response:**
```json
{
    "error": "Error message here"
}
```