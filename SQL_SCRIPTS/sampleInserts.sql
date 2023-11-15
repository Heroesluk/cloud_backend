INSERT INTO users (username, password_hash, email)
VALUES ('user1', 'hashed_password_1', 'user1@example.com'),
       ('user2', 'hashed_password_2', 'user2@example.com'),
       ('user3', 'hashed_password_3', 'user3@example.com');

INSERT INTO images (user_id, folder_name, image_size, image_add_date)
VALUES (1, 'user1', 1024, '2023-01-01 12:00:00'),
       (1, 'user1', 2048, '2023-01-02 14:30:00'),
       (2, 'user2', 1536, '2023-01-03 10:45:00'),
       (2, 'user2', 3072, '2023-01-04 08:15:00'),
       (3, 'user3', 1024, '2023-01-05 16:00:00');