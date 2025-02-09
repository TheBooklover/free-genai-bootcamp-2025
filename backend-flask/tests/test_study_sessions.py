import pytest
from datetime import datetime

def test_create_study_session_success(client, app, test_group, test_activity):
    # Test the POST endpoint
    response = client.post('/api/study-sessions', json={
        'group_id': test_group,
        'study_activity_id': test_activity
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert data['group_id'] == test_group
    assert data['group_name'] == 'Test Group'
    assert data['activity_id'] == test_activity
    assert data['activity_name'] == 'Test Activity'
    assert 'start_time' in data
    assert 'end_time' in data
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

# Add more test cases as needed 