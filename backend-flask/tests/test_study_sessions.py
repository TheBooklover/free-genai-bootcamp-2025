import pytest
from datetime import datetime

def test_create_study_session_success(client):
    """Test successful creation of a study session"""
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 1
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert 'group_name' in data
    assert 'activity_name' in data
    assert 'start_time' in data
    assert 'review_items_count' in data
    assert data['review_items_count'] == 0

def test_create_study_session_missing_fields(client):
    # Test missing study_activity_id
    response = client.post('/api/study-sessions', json={
        'group_id': 1
        # missing study_activity_id
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Missing required field: study_activity_id' in data['error']
    
    # Test missing group_id
    response = client.post('/api/study-sessions', json={
        'study_activity_id': 1
        # missing group_id
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Missing required field: group_id' in data['error']

def test_create_study_session_invalid_ids(client):
    # Test invalid group_id
    response = client.post('/api/study-sessions', json={
        'group_id': 99999,  # non-existent group
        'study_activity_id': 1
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Group not found' in data['error']
    
    # Test invalid study_activity_id
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 99999  # non-existent activity
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Study activity not found' in data['error']

def test_create_study_session_malformed_request(client):
    # Test with non-JSON data
    response = client.post('/api/study-sessions', data='not json')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data

def test_submit_review_success(client, app):
    """Test successful submission of a word review"""
    # Setup test data
    with app.db.cursor() as cursor:
        # Create a test study session
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (1, 1, ?)
        ''', (datetime.now(),))
        session_id = cursor.lastrowid
        
        # Create a test word
        cursor.execute('''
            INSERT INTO words (quebecois, standard_french, english)
            VALUES (?, ?, ?)
        ''', ('pogner', 'attraper', 'to catch/grab'))
        word_id = cursor.lastrowid
        
        app.db.commit()
    
    # Test the endpoint
    response = client.post(f'/api/study-sessions/{session_id}/review', json={
        'word_id': word_id,
        'correct': True
    })
    
    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert data['word_id'] == word_id
    assert data['correct'] == True
    assert data['quebecois'] == 'pogner'
    assert data['standard_french'] == 'attraper'
    assert data['english'] == 'to catch/grab'
    assert 'reviewed_at' in data

def test_submit_review_invalid_session(client, app):
    """Test review submission with non-existent session"""
    # Setup test word
    with app.db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO words (quebecois, standard_french, english)
            VALUES (?, ?, ?)
        ''', ('pogner', 'attraper', 'to catch/grab'))
        word_id = cursor.lastrowid
        app.db.commit()
    
    response = client.post('/api/study-sessions/999/review', json={
        'word_id': word_id,
        'correct': True
    })
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Study session not found'

def test_submit_review_invalid_word(client, app):
    """Test review submission with non-existent word"""
    # Setup test session
    with app.db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (1, 1, ?)
        ''', (datetime.now(),))
        session_id = cursor.lastrowid
        app.db.commit()
    
    response = client.post(f'/api/study-sessions/{session_id}/review', json={
        'word_id': 999,
        'correct': True
    })
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Word not found'

def test_submit_review_invalid_data(client, app):
    """Test review submission with invalid request data"""
    # Setup test session
    with app.db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (1, 1, ?)
        ''', (datetime.now(),))
        session_id = cursor.lastrowid
        app.db.commit()
    
    # Test missing correct field
    response = client.post(f'/api/study-sessions/{session_id}/review', json={
        'word_id': 1
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Missing correct field'
    
    # Test invalid correct field type
    response = client.post(f'/api/study-sessions/{session_id}/review', json={
        'word_id': 1,
        'correct': 'not a boolean'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'correct field must be a boolean'

def test_get_study_sessions(client):
    """Test fetching paginated study sessions"""
    response = client.get('/api/study-sessions')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data
    assert 'page' in data
    assert 'per_page' in data
    assert 'total_pages' in data

def test_get_study_session_details(client):
    """Test fetching single study session details"""
    # First create a session
    create_response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 1
    })
    session_id = create_response.get_json()['id']

    # Then fetch its details
    response = client.get(f'/api/study-sessions/{session_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert 'session' in data
    assert 'words' in data
    assert data['session']['id'] == session_id

def test_submit_session_review_success(client):
    """Test successful submission of batch reviews"""
    # First create a session
    create_response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 1
    })
    session_id = create_response.get_json()['id']

    # Submit batch reviews
    reviews = [
        {'word_id': 1, 'correct': True},
        {'word_id': 2, 'correct': False}
    ]
    response = client.post(
        f'/api/study-sessions/{session_id}/review',
        json={'reviews': reviews}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'reviews' in data
    assert len(data['reviews']) == 2
    
    # Verify review data
    for review in data['reviews']:
        assert 'id' in review
        assert 'word_id' in review
        assert 'kanji' in review
        assert 'romaji' in review
        assert 'english' in review
        assert 'correct' in review
        assert 'reviewed_at' in review

def test_submit_session_review_validation(client):
    """Test review submission validation"""
    session_id = 1
    invalid_payloads = [
        # Missing reviews array
        {},
        # Empty reviews array
        {'reviews': []},
        # Invalid review object
        {'reviews': [{'word_id': 1}]},
        # Invalid word_id type
        {'reviews': [{'word_id': 'abc', 'correct': True}]},
        # Invalid correct type
        {'reviews': [{'word_id': 1, 'correct': 'yes'}]}
    ]

    for payload in invalid_payloads:
        response = client.post(
            f'/api/study-sessions/{session_id}/review',
            json=payload
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

def test_submit_session_review_not_found(client):
    """Test review submission for non-existent session"""
    response = client.post(
        '/api/study-sessions/99999/review',
        json={'reviews': [{'word_id': 1, 'correct': True}]}
    )
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'Study session not found' in data['error']

def test_reset_study_sessions(client):
    """Test clearing study history"""
    # First create a session and submit some reviews
    create_response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 1
    })
    session_id = create_response.get_json()['id']
    
    client.post(
        f'/api/study-sessions/{session_id}/review',
        json={'reviews': [{'word_id': 1, 'correct': True}]}
    )

    # Then reset all sessions
    response = client.post('/api/study-sessions/reset')
    assert response.status_code == 200
    
    # Verify sessions are cleared
    sessions_response = client.get('/api/study-sessions')
    data = sessions_response.get_json()
    assert data['total'] == 0
    assert len(data['items']) == 0

# Add more test cases as needed 