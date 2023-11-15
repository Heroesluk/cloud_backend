CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    folder_name VARCHAR(50) NOT NULL,
    image_size INTEGER NOT NULL,
    image_add_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);