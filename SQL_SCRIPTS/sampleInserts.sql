INSERT INTO users (username, password_hash, email)
VALUES ('user1', 'hashed_password_1', 'user1@example.com'),
       ('user2', 'hashed_password_2', 'user2@example.com'),
       ('user3', 'hashed_password_3', 'user3@example.com');


INSERT INTO images (image_id, image_name, folder_id, image_size, image_add_date)
VALUES (1, 'image1.jpg', 1, 1024, '2023-01-01 12:00:00'),
       (2, 'image2.jpg', 1, 2048, '2023-01-02 14:30:00'),
       (3, 'image3.jpg', 1, 1536, '2023-01-03 10:45:00'),
       (4, 'image4.jpg', 2, 3072, '2023-01-04 08:15:00'),
       (5, 'image5.jpg', 3, 1024, '2023-01-05 16:00:00');