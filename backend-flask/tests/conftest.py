import pytest
from datetime import datetime
from app import create_app  # Make sure this import works with your app structure

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app, setup_test_data):
    """A test client for the app with test data."""
    return app.test_client()

@pytest.fixture
def test_group(app):
    """Creates a test group and returns its ID"""
    with app.db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO groups (name, created_at)
            VALUES (?, ?)
        ''', ('Test Group', datetime.now()))
        group_id = cursor.lastrowid
        app.db.commit()
        
        yield group_id  # The test uses this value
        
        # Cleanup after test
        cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
        app.db.commit()

@pytest.fixture
def test_activity(app):
    """Creates a test study activity and returns its ID"""
    with app.db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO study_activities (name, created_at)
            VALUES (?, ?)
        ''', ('Test Activity', datetime.now()))
        activity_id = cursor.lastrowid
        app.db.commit()
        
        yield activity_id  # The test uses this value
        
        # Cleanup after test
        cursor.execute('DELETE FROM study_activities WHERE id = ?', (activity_id,))
        app.db.commit()

@pytest.fixture
def setup_test_data(app):
    """Set up test data for study sessions"""
    cursor = app.db.cursor()
    
    # Add test group
    cursor.execute('''
        INSERT INTO groups (name) VALUES (?)
    ''', ('Test Group',))
    
    # Add test activity
    cursor.execute('''
        INSERT INTO study_activities (name, url, preview_url)
        VALUES (?, ?, ?)
    ''', ('Test Activity', 'http://test.com', 'http://test.com/preview'))
    
    # Add test words
    cursor.execute('''
        INSERT INTO words (kanji, romaji, english)
        VALUES 
        (?, ?, ?),
        (?, ?, ?)
    ''', ('漢字1', 'kanji1', 'test1', '漢字2', 'kanji2', 'test2'))
    
    app.db.commit() 