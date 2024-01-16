CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE images
(
    image_id       SERIAL PRIMARY KEY,
    image_name     TEXT    NOT NULL,
    folder_id      INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    image_size     INTEGER NOT NULL,
    image_add_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE Logger (
    id SERIAL PRIMARY KEY,
    severity VARCHAR(255),
    timestamp VARCHAR(255),
    message VARCHAR(255)
);