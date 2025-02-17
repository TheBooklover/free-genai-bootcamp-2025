import pytest
from datetime import datetime
import sys
import os
import tempfile
from app import create_app
from lib.db import Db

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    """Create and configure a test Flask app instance"""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Create the app with test config
    test_app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    # Set up the database and create tables
    with test_app.app_context():
        cursor = test_app.db.cursor()
        
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER NOT NULL,
                correct_count INTEGER DEFAULT 0,
                wrong_count INTEGER DEFAULT 0,
                FOREIGN KEY (word_id) REFERENCES words(id)
            )
        ''')
        
        test_app.db.commit()

    yield test_app

    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def test_group(app):
    """Create a test group and return its ID"""
    with app.app_context():
        cursor = app.db.cursor()
        
        # Insert test group
        cursor.execute('''
            INSERT INTO groups (name, words_count)
            VALUES (?, ?)
        ''', ('Test Group', 0))
        group_id = cursor.lastrowid
        app.db.commit()
        
        yield group_id
        
        # Clean up
        cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
        app.db.commit()

@pytest.fixture
def test_activity(app):
    """Create a test activity and return its ID"""
    with app.app_context():
        cursor = app.db.cursor()
        
        # Insert test activity
        cursor.execute('''
            INSERT INTO study_activities (name, created_at)
            VALUES (?, ?)
        ''', ('Test Activity', datetime.now()))
        activity_id = cursor.lastrowid
        app.db.commit()
        
        yield activity_id
        
        # Clean up
        cursor.execute('DELETE FROM study_activities WHERE id = ?', (activity_id,))
        app.db.commit()

@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner() 