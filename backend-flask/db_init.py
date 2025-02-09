import sqlite3
import os

def init_db():
    db = sqlite3.connect('words.db')
    
    # Read and execute the migration
    with open('migrations/03_update_words_for_quebecois.sql') as f:
        db.executescript(f.read())
    
    db.close()

if __name__ == '__main__':
    init_db() 