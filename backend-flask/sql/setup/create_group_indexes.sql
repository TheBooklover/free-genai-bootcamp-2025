-- Create indexes for groups table
CREATE INDEX IF NOT EXISTS idx_groups_name ON groups(name);
CREATE INDEX IF NOT EXISTS idx_groups_words_count ON groups(words_count); 