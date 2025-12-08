-- SQL script to create the saves and likes tables in PostgreSQL

-- Create the saves table
CREATE TABLE IF NOT EXISTS saves (
    id SERIAL PRIMARY KEY,
    std_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    saved_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(std_id, topic_id),
    FOREIGN KEY (std_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);

-- Create the likes table
CREATE TABLE IF NOT EXISTS likes (
    id SERIAL PRIMARY KEY,
    std_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    UNIQUE(std_id, topic_id),
    FOREIGN KEY (std_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_saves_std_id ON saves(std_id);
CREATE INDEX IF NOT EXISTS idx_saves_topic_id ON saves(topic_id);
CREATE INDEX IF NOT EXISTS idx_likes_std_id ON likes(std_id);
CREATE INDEX IF NOT EXISTS idx_likes_topic_id ON likes(topic_id);
