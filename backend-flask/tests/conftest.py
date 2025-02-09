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
def client(app):
    """A test client for the app."""
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