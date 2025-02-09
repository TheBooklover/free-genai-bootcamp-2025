-- First backup the existing data if needed
CREATE TABLE IF NOT EXISTS words_backup AS SELECT * FROM words;

-- Drop existing word-related foreign key constraints
DROP TABLE IF EXISTS word_groups;
DROP TABLE IF EXISTS word_reviews;

-- Drop and recreate the words table with new structure
DROP TABLE IF EXISTS words;
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quebecois TEXT NOT NULL,           -- Québécois French word/phrase
    standard_french TEXT NOT NULL,      -- Standard French equivalent
    english TEXT NOT NULL,             -- English translation
    pronunciation TEXT,                -- IPA or phonetic pronunciation guide
    usage_notes TEXT,                  -- Cultural context and usage examples
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recreate the related tables
CREATE TABLE word_reviews (
    word_id INTEGER NOT NULL,
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    last_reviewed_at TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words (id) ON DELETE CASCADE
);

CREATE TABLE word_groups (
    word_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words (id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
    PRIMARY KEY (word_id, group_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_words_quebecois ON words(quebecois);
CREATE INDEX idx_words_standard_french ON words(standard_french);
CREATE INDEX idx_words_english ON words(english);
CREATE INDEX idx_word_reviews_word_id ON word_reviews(word_id);
CREATE INDEX idx_word_groups_word_id ON word_groups(word_id);
CREATE INDEX idx_word_groups_group_id ON word_groups(group_id);

-- Insert some sample Québécois French words
INSERT INTO words (quebecois, standard_french, english, pronunciation, usage_notes) VALUES 
    ('char', 'voiture', 'car', 'ʃaʁ', 'Very common in Quebec. Used in the same way as "voiture" in standard French.'),
    ('pogner', 'attraper', 'to catch/grab', 'pɔɲe', 'Extremely common Quebec verb. Also used figuratively: "Je te pogne!" (I get what you mean!)'),
    ('tuque', 'bonnet', 'winter hat/beanie', 'tʏk', 'Essential Quebec winter vocabulary. Symbol of Quebec culture.'),
    ('dépanneur', 'épicerie', 'convenience store', 'depanœʁ', 'Often shortened to "dép". Corner stores unique to Quebec culture.');

-- Trigger to update the updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_words_timestamp 
    AFTER UPDATE ON words
    BEGIN
        UPDATE words SET updated_at = CURRENT_TIMESTAMP 
        WHERE id = NEW.id;
    END; 