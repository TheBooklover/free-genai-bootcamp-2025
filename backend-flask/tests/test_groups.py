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
    
    # Set up the database and create tables
    with app.app_context():
        cursor = app.db.cursor()
        
        # Create groups table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                words_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create words table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quebecois TEXT NOT NULL,
                standard_french TEXT NOT NULL,
                english TEXT NOT NULL,
                pronunciation TEXT,
                usage_notes TEXT
            )
        ''')
        
        # Create word_groups table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_groups (
                word_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                FOREIGN KEY (word_id) REFERENCES words(id),
                FOREIGN KEY (group_id) REFERENCES groups(id),
                PRIMARY KEY (word_id, group_id)
            )
        ''')
        
        # Create word_reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_reviews (
                word_id INTEGER NOT NULL,
                correct_count INTEGER DEFAULT 0,
                wrong_count INTEGER DEFAULT 0,
                FOREIGN KEY (word_id) REFERENCES words(id)
            )
        ''')
        
        app.db.commit()
    
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

def test_get_group_words_raw_empty_group(client, app):
    """Test fetching raw words from an empty group"""
    with app.app_context():
        cursor = app.db.cursor()
        
        # Create required tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                words_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quebecois TEXT NOT NULL,
                standard_french TEXT NOT NULL,
                english TEXT NOT NULL,
                pronunciation TEXT,
                usage_notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_groups (
                word_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                FOREIGN KEY (word_id) REFERENCES words(id),
                FOREIGN KEY (group_id) REFERENCES groups(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_reviews (
                word_id INTEGER NOT NULL,
                correct_count INTEGER DEFAULT 0,
                wrong_count INTEGER DEFAULT 0,
                FOREIGN KEY (word_id) REFERENCES words(id)
            )
        ''')
        
        # Create a test group
        cursor.execute('''
            INSERT INTO groups (name, words_count)
            VALUES (?, ?)
        ''', ('Empty Test Group', 0))
        group_id = cursor.lastrowid
        app.db.commit()
        
        # Test fetching words from empty group
        response = client.get(f'/groups/{group_id}/words/raw')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'words' in data
        assert len(data['words']) == 0
        assert data['total_count'] == 0

        # Cleanup
        cursor.execute('DROP TABLE IF EXISTS word_groups')
        cursor.execute('DROP TABLE IF EXISTS word_reviews')
        cursor.execute('DROP TABLE IF EXISTS words')
        cursor.execute('DROP TABLE IF EXISTS groups')
        app.db.commit()

def test_get_group_words_raw_success(client, app):
    """Test successful fetching of raw words from a group"""
    with app.app_context():
        cursor = app.db.cursor()
        
        # Create required tables first
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                words_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quebecois TEXT NOT NULL,
                standard_french TEXT NOT NULL,
                english TEXT NOT NULL,
                pronunciation TEXT,
                usage_notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_groups (
                word_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                FOREIGN KEY (word_id) REFERENCES words(id),
                FOREIGN KEY (group_id) REFERENCES groups(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_reviews (
                word_id INTEGER NOT NULL,
                correct_count INTEGER DEFAULT 0,
                wrong_count INTEGER DEFAULT 0,
                FOREIGN KEY (word_id) REFERENCES words(id)
            )
        ''')
        
        # Create test group
        cursor.execute('''
            INSERT INTO groups (name, words_count)
            VALUES (?, ?)
        ''', ('Test Group', 2))
        group_id = cursor.lastrowid

        # Create test words
        cursor.execute('''
            INSERT INTO words (quebecois, standard_french, english, pronunciation, usage_notes)
            VALUES 
            (?, ?, ?, ?, ?),
            (?, ?, ?, ?, ?)
        ''', (
            'char', 'voiture', 'car', 'ʃaʁ', 'Common in Quebec',
            'pogner', 'attraper', 'to catch', 'pɔɲe', 'Informal usage'
        ))
        
        # Link words to group
        word_ids = [cursor.lastrowid - 1, cursor.lastrowid]
        for word_id in word_ids:
            cursor.execute('''
                INSERT INTO word_groups (word_id, group_id)
                VALUES (?, ?)
            ''', (word_id, group_id))
        
        app.db.commit()

        # Test fetching words
        response = client.get(f'/groups/{group_id}/words/raw')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'words' in data
        assert 'total_count' in data
        assert data['total_count'] == 2
        
        words = data['words']
        assert len(words) == 2
        
        # Verify word fields
        for word in words:
            assert 'id' in word
            assert 'quebecois' in word
            assert 'standard_french' in word
            assert 'english' in word
            assert 'pronunciation' in word
            assert 'usage_notes' in word
            assert 'correct_count' in word
            assert 'wrong_count' in word

        # Verify specific word data
        assert any(w['quebecois'] == 'char' for w in words)
        assert any(w['quebecois'] == 'pogner' for w in words)

        # Cleanup
        cursor.execute('DELETE FROM word_groups WHERE group_id = ?', (group_id,))
        cursor.execute('DELETE FROM words WHERE id IN (?, ?)', (word_ids[0], word_ids[1]))
        cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
        cursor.execute('DROP TABLE IF EXISTS word_groups')
        cursor.execute('DROP TABLE IF EXISTS word_reviews')
        cursor.execute('DROP TABLE IF EXISTS words')
        cursor.execute('DROP TABLE IF EXISTS groups')
        app.db.commit()

def test_get_group_words_raw_nonexistent(client, app):
    """Test fetching raw words from a non-existent group"""
    with app.app_context():
        cursor = app.db.cursor()
        
        # Create groups table so we can properly check for non-existent ID
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                words_count INTEGER DEFAULT 0
            )
        ''')
        
        # Test with non-existent group ID
        response = client.get('/groups/99999/words/raw')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Group not found'
        
        # Cleanup
        cursor.execute('DROP TABLE IF EXISTS groups')
        app.db.commit() 