import pytest
from app import create_app
import json

@pytest.fixture
def app():
    """Create and configure a test Flask app instance"""
    app = create_app({
        'TESTING': True,
        'DATABASE': 'test_words.db'
    })
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

def test_get_words_basic(client):
    """Test basic word retrieval without parameters"""
    response = client.get('/api/words')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'words' in data
    assert 'total_pages' in data
    assert 'current_page' in data
    assert 'total_words' in data

def test_get_words_pagination(client):
    """Test pagination parameters"""
    # Test first page
    response = client.get('/api/words?page=1&per_page=10')
    data = json.loads(response.data)
    assert len(data['words']) <= 10
    assert data['current_page'] == 1
    
    # Test second page
    response = client.get('/api/words?page=2&per_page=10')
    data = json.loads(response.data)
    assert data['current_page'] == 2

def test_get_words_sorting(client):
    """Test sorting functionality"""
    # Test ascending sort
    response = client.get('/api/words?sort_by=quebecois&order=asc')
    data_asc = json.loads(response.data)
    
    # Test descending sort
    response = client.get('/api/words?sort_by=quebecois&order=desc')
    data_desc = json.loads(response.data)
    
    # Verify different ordering
    if len(data_asc['words']) > 0 and len(data_desc['words']) > 0:
        assert data_asc['words'][0] != data_desc['words'][0]

def test_get_words_search(client):
    """Test search functionality"""
    response = client.get('/api/words?search=test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'words' in data

def test_get_words_error_cases(client):
    """Test error handling"""
    # Test invalid page number
    response = client.get('/api/words?page=invalid')
    assert response.status_code == 400
    
    # Test invalid sort column
    response = client.get('/api/words?sort_by=invalid_column')
    assert response.status_code == 400
    
    # Test invalid sort order
    response = client.get('/api/words?order=invalid')
    assert response.status_code == 400
    
    # Test invalid per_page value
    response = client.get('/api/words?per_page=1000')
    data = json.loads(response.data)
    assert len(data['words']) <= 100  # Should be capped at max 100

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

def test_get_word_not_found(client):
    """Test getting a non-existent word"""
    response = client.get('/api/words/99999')
    assert response.status_code == 404 