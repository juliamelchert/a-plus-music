SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- EDITS: 
--   - Artists name changed to NOT NULL
--   - Song_Reviews and Album_Reviews review bodies changed to DEFAULT NULL
--   - ON DELETE CASCADES added
--   - added default 0.0 values to avg attributes

----- TABLE CREATION -----

CREATE OR REPLACE TABLE Users (
    user_id int NOT NULL AUTO_INCREMENT,
    username varchar(45) UNIQUE NOT NULL,
    email varchar(30) UNIQUE NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE OR REPLACE TABLE Artists (
    artist_id int NOT NULL AUTO_INCREMENT,
    name varchar(45) NOT NULL,
    PRIMARY KEY (artist_id)
);

CREATE OR REPLACE TABLE Albums (
    album_id int NOT NULL AUTO_INCREMENT,
    artist_id int NOT NULL,
    avg_album_rating decimal(2, 1) NOT NULL DEFAULT 0.0,
    album_title varchar(125) NOT NULL,
    album_genre varchar(24) NOT NULL,
    PRIMARY KEY (album_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

CREATE OR REPLACE TABLE Songs (
    song_id int NOT NULL AUTO_INCREMENT,
    artist_id int NOT NULL,
    avg_song_rating decimal(2, 1) NOT NULL DEFAULT 0.0,
    song_title varchar(125) NOT NULL,
    song_genre varchar(24) NOT NULL,
    PRIMARY KEY (song_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

CREATE OR REPLACE TABLE Song_Reviews (
    song_review_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    song_id int NOT NULL,
    song_rating tinyint NOT NULL,
    song_review_body text DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES Songs(song_id) ON DELETE CASCADE,
    PRIMARY KEY (song_review_id)
);

CREATE OR REPLACE TABLE Album_Reviews (
    album_review_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    album_id int NOT NULL,
    album_rating tinyint NOT NULL,
    album_review_body text DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id),
    PRIMARY KEY (album_review_id)
);

CREATE OR REPLACE TABLE Albums_Songs (
    album_song_id int NOT NULL AUTO_INCREMENT,
    album_id int NOT NULL,
    song_id int NOT NULL,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id),
    PRIMARY KEY (album_song_id)
);



----- TEST CODE FOR TABLE CREATION -----

-- DESCRIBE Albums;
-- DESCRIBE Songs;
-- DESCRIBE Artists;
-- DESCRIBE Users;
-- DESCRIBE Song_Reviews;
-- DESCRIBE Album_Reviews;
-- DESCRIBE Albums_Songs;



----- INSERT SAMPLE DATA -----

INSERT INTO Artists (name) VALUES
('Michael Jackson'),
('Earth, Wind & Fire'),
('Pink Floyd'),
('Chick Corea and Return to Forever'),
('"Weird Al" Yankovic');

INSERT INTO Users (username, email) VALUES
('user1', 'user1@hello.com'),
('user2', 'user2@hello.com'),
('user3', 'user3@hello.com');

INSERT INTO Albums (artist_id, avg_album_rating, album_title, album_genre) VALUES
((SELECT artist_id FROM Artists WHERE name = '"Weird Al" Yankovic'), 3.9, 'Even Worse', 'Comedy'),
((SELECT artist_id FROM Artists WHERE name = 'Chick Corea and Return to Forever'), 4.2, 'Light as a Feather', 'Jazz Fusion'),
((SELECT artist_id FROM Artists WHERE name = 'Pink Floyd'), 5.0, 'The Dark Side of the Moon', 'Prog. Rock'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 4.4, 'The Best of Earth, Wind & Fire Vol. 1', 'R&B'),
((SELECT artist_id FROM Artists WHERE name = 'Michael Jackson'), 4.8, 'Thriller', 'Pop'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 4.1, 'September (Single)', 'R&B');

INSERT INTO Songs (artist_id, avg_song_rating, song_title, song_genre) VALUES
((SELECT artist_id FROM Artists WHERE name = 'Michael Jackson'), 4.5, 'Thriller', 'Pop'),
((SELECT artist_id FROM Artists WHERE name = 'Michael Jackson'), 4.7, 'Beat It', 'Comedy'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 4.9, 'September', 'R&B'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 3.8, 'Fantasy', 'R&B'),
((SELECT artist_id FROM Artists WHERE name = 'Pink Floyd'), 4.5, 'Time', 'Prog. Rock'),
((SELECT artist_id FROM Artists WHERE name = 'Pink Floyd'), 4.7, 'Money', 'Prog. Rock'),
((SELECT artist_id FROM Artists WHERE name = 'Chick Corea and Return to Forever'), 4.2, 'Light as a Feather', 'Jazz Fusion'),
((SELECT artist_id FROM Artists WHERE name = 'Chick Corea and Return to Forever'), 4.9, 'Spain', 'Jazz Fusion'),
((SELECT artist_id FROM Artists WHERE name = '"Weird Al" Yankovic'), 3.8, 'Lasagna', 'Comedy'),
((SELECT artist_id FROM Artists WHERE name = '"Weird Al" Yankovic'), 4.8, 'Fat', 'Comedy');

INSERT INTO Song_Reviews (user_id, song_id, song_rating, song_review_body) VALUES
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT song_id FROM Songs WHERE song_title = 'Thriller'), 5, "There's a reason why Michael Jackson is known as the King of Pop!"),
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT song_id FROM Songs WHERE song_title = 'September'), 5, '"Do you remember, the 21st night of September?"'),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT song_id FROM Songs WHERE song_title = 'Spain'), 5, 'RIP Chick Corea. You truly pushed the boundaries of Jazz and created such an amazing Jazz standard.'),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT song_id FROM Songs WHERE song_title = 'September'), 5, NULL),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT song_id FROM Songs WHERE song_title = 'Money'), 5, NULL),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT song_id FROM Songs WHERE song_title = 'Fat'), 5, '"He who is tired of Weird Al is tired of life." - Homer Simpson');

INSERT INTO Album_Reviews (user_id, album_id, album_rating, album_review_body) VALUES
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT album_id FROM Albums WHERE album_title = 'Thriller'), 5, "C'mon, Thriller AND Beat It are on this album! 5/5"),
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT album_id FROM Albums WHERE album_title = 'The Best of Earth, Wind & Fire Vol. 1'), 5, 'Love me some Earth, Wind & Fire.'),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT album_id FROM Albums WHERE album_title = 'Light as a Feather'), 4, "I'm a huge fan of Spain, but I don't think the entire album is a hit."),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT album_id FROM Albums WHERE album_title = 'September (Single)'), 5, 'September was good enough as a single. Enough said.'),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT album_id FROM Albums WHERE album_title = 'The Dark Side of the Moon'), 5, 'You have to listen to the whole album at once.'),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT album_id FROM Albums WHERE album_title = 'Even Worse'), 4, NULL);

INSERT INTO Albums_Songs (album_id, song_id) VALUES
((SELECT album_id FROM Albums WHERE album_title = 'Even Worse'), (SELECT song_id FROM Songs WHERE song_title = 'Lasagna')),
((SELECT album_id FROM Albums WHERE album_title = 'Even Worse'), (SELECT song_id FROM Songs WHERE song_title = 'Fat')),
((SELECT album_id FROM Albums WHERE album_title = 'Light as a Feather'), (SELECT song_id FROM Songs WHERE song_title = 'Light as a Feather')),
((SELECT album_id FROM Albums WHERE album_title = 'Light as a Feather'), (SELECT song_id FROM Songs WHERE song_title = 'Spain')),
((SELECT album_id FROM Albums WHERE album_title = 'The Dark Side of the Moon'), (SELECT song_id FROM Songs WHERE song_title = 'Time')),
((SELECT album_id FROM Albums WHERE album_title = 'The Dark Side of the Moon'), (SELECT song_id FROM Songs WHERE song_title = 'Money')),
((SELECT album_id FROM Albums WHERE album_title = 'The Best of Earth, Wind & Fire Vol. 1'), (SELECT song_id FROM Songs WHERE song_title = 'September')),
((SELECT album_id FROM Albums WHERE album_title = 'The Best of Earth, Wind & Fire Vol. 1'), (SELECT song_id FROM Songs WHERE song_title = 'Fantasy')),
((SELECT album_id FROM Albums WHERE album_title = 'Thriller'), (SELECT song_id FROM Songs WHERE song_title = 'Thriller')),
((SELECT album_id FROM Albums WHERE album_title = 'Thriller'), (SELECT song_id FROM Songs WHERE song_title = 'Beat It')),
((SELECT album_id FROM Albums WHERE album_title = 'September (Single)'), (SELECT song_id FROM Songs WHERE song_title = 'September'));



----- TEST CODE FOR DATA INSERTION -----

-- SELECT * FROM Albums;
-- SELECT * FROM Songs;
-- SELECT * FROM Artists;
-- SELECT * FROM Users;
-- SELECT * FROM Song_Reviews;
-- SELECT * FROM Album_Reviews;
-- SELECT * FROM Albums_Songs;

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;