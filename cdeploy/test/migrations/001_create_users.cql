CREATE TABLE users (userid uuid PRIMARY KEY, title text);
CREATE INDEX users_title_index ON users(title);
