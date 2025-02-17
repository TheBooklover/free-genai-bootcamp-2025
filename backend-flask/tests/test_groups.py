import pytest
from app import create_app
import json

@pytest.fixture
def app():
    """Create and configure a test Flask app instance"""
    app = create_app({
        'TESTING': True,
        'DATABASE': ':memory:'  # Use in-memory SQLite for testing
    })
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()

def test_get_groups_pagination(client, app):
    """Test pagination of groups endpoint"""
    with app.app_context():
        # Create table and test data
        cursor = app.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                words_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        for i in range(15):  # Create 15 groups to test pagination
            cursor.execute('''
                INSERT INTO groups (name, words_count)
                VALUES (?, ?)
            ''', (f'Test Group {i}', 0))
        app.db.commit()

        # Test first page
        response = client.get('/groups?page=1&per_page=10')
        data = json.loads(response.data)
        assert len(data['groups']) == 10
        assert data['current_page'] == 1
        assert data['total_pages'] == 2
        
        # Test second page
        response = client.get('/groups?page=2&per_page=10')
        data = json.loads(response.data)
        assert len(data['groups']) == 5
        assert data['current_page'] == 2

        # Cleanup
        cursor.execute('DROP TABLE IF EXISTS groups')
        app.db.commit()

def test_get_groups_sorting(client, app):
    """Test sorting of groups endpoint"""
    with app.app_context():
        # Create table and test data
        cursor = app.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                words_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            INSERT INTO groups (name, words_count)
            VALUES (?, ?), (?, ?)
        ''', ('B Test Group', 0, 'A Test Group', 0))
        app.db.commit()
        
        # Test sorting by name ascending
        response = client.get('/groups?sort_by=name&order=asc')
        data = json.loads(response.data)
        names = [g['group_name'] for g in data['groups']]
        assert names == sorted(names)

        # Cleanup
        cursor.execute('DROP TABLE IF EXISTS groups')
        app.db.commit()

def test_get_groups_search(client, app):
    """Test search filtering of groups endpoint"""
    with app.app_context():
        # Create table and test data
        cursor = app.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                words_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        test_groups = [
            ('Test Alpha Group', 10),
            ('Test Beta Group', 5),
            ('Production Group', 15)
        ]
        for name, count in test_groups:
            cursor.execute('''
                INSERT INTO groups (name, words_count)
                VALUES (?, ?)
            ''', (name, count))
        app.db.commit()
        
        # Test searching for 'Test' groups
        response = client.get('/groups?search=Test')
        data = json.loads(response.data)
        groups = data['groups']
        assert len(groups) == 2
        assert all('Test' in g['group_name'] for g in groups)

        # Cleanup
        cursor.execute('DROP TABLE IF EXISTS groups')
        app.db.commit()

def test_get_groups_error_cases(client, app):
    """Test error cases for groups endpoint"""
    with app.app_context():
        # Test invalid page number
        response = client.get('/groups?page=0')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
        # Test invalid sort column
        response = client.get('/groups?sort_by=invalid_column')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
        # Test non-integer page number
        response = client.get('/groups?page=abc')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data 