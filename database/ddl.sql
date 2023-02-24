-- Group 86 Jeffrey Wang and Julia Melchert

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- CREATING TABLES
-- Create Users
CREATE OR REPLACE TABLE Users (
    user_id int NOT NULL AUTO_INCREMENT,
    username varchar(45) UNIQUE NOT NULL,
    email varchar(50) UNIQUE NOT NULL,
    PRIMARY KEY (user_id)
);

-- Create Artists
CREATE OR REPLACE TABLE Artists (
    artist_id int NOT NULL AUTO_INCREMENT,
    name varchar(45) NOT NULL,
    PRIMARY KEY (artist_id)
);

-- Create Albums
CREATE OR REPLACE TABLE Albums (
    album_id int NOT NULL AUTO_INCREMENT,
    artist_id int NOT NULL,
    avg_album_rating decimal(2, 1) NOT NULL DEFAULT 0.0,
    album_title varchar(125) NOT NULL,
    album_genre varchar(24) NOT NULL,
    PRIMARY KEY (album_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

-- Create Songs table
CREATE OR REPLACE TABLE Songs (
    song_id int NOT NULL AUTO_INCREMENT,
    artist_id int NOT NULL,
    avg_song_rating decimal(2, 1) NOT NULL DEFAULT 0.0,
    song_title varchar(125) NOT NULL,
    song_genre varchar(24) NOT NULL,
    PRIMARY KEY (song_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

-- Create Song_Review table
CREATE OR REPLACE TABLE Song_Reviews (
    song_review_id int NOT NULL AUTO_INCREMENT,
    user_id int,
    song_id int NOT NULL,
    song_rating tinyint NOT NULL,
    song_review_body text DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL,  -- Set User as NULL if User doesn't exist
    FOREIGN KEY (song_id) REFERENCES Songs(song_id) ON DELETE CASCADE,  -- Delete review if Song doesn't exist
    PRIMARY KEY (song_review_id)
);

-- Create Album_Reviews table
CREATE OR REPLACE TABLE Album_Reviews (
    album_review_id int NOT NULL AUTO_INCREMENT,
    user_id int,
    album_id int NOT NULL,
    album_rating tinyint NOT NULL,
    album_review_body text DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL,  -- Set User as NULL if User doesn't exist
    FOREIGN KEY (album_id) REFERENCES Albums(album_id) ON DELETE CASCADE,  -- Delete review if Album doesn't exist
    PRIMARY KEY (album_review_id)
);

-- Create Albums_Songs intersection table
CREATE OR REPLACE TABLE Albums_Songs (
    album_song_id int NOT NULL AUTO_INCREMENT,
    album_id int NOT NULL,
    song_id int NOT NULL,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id) ON DELETE CASCADE,  -- Delete reference if Album doesn't exist
    FOREIGN KEY (song_id) REFERENCES Songs(song_id) ON DELETE CASCADE,  -- Delete reference if Song doesn't exist
    CONSTRAINT FK_pair UNIQUE (album_id, song_id),  -- don't duplicate FK pairs
    PRIMARY KEY (album_song_id)
);

-- DESCRIBE Albums;
-- DESCRIBE Songs;
-- DESCRIBE Artists;
-- DESCRIBE Users;
-- DESCRIBE Song_Reviews;
-- DESCRIBE Album_Reviews;
-- DESCRIBE Albums_Songs;


-- INSERT DUMMY DATA

-- Insert Dummy Artists Data
INSERT INTO Artists (name) VALUES
('Michael Jackson'),
('Earth, Wind & Fire'),
('Pink Floyd'),
('Chick Corea and Return to Forever'),
('"Weird Al" Yankovic');


-- Insert Dummy Users Data
INSERT INTO Users (username, email) VALUES
('user1', 'user1@hello.com'),
('user2', 'user2@hello.com'),
('user3', 'user3@hello.com');


-- Insert Dummy Albums Data
INSERT INTO Albums (artist_id, album_title, album_genre) VALUES
((SELECT artist_id FROM Artists WHERE name = '"Weird Al" Yankovic'), 'Even Worse', 'Comedy'),
((SELECT artist_id FROM Artists WHERE name = 'Chick Corea and Return to Forever'), 'Light as a Feather', 'Jazz Fusion'),
((SELECT artist_id FROM Artists WHERE name = 'Pink Floyd'), 'The Dark Side of the Moon', 'Prog. Rock'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 'The Best of Earth, Wind & Fire Vol. 1', 'R&B'),
((SELECT artist_id FROM Artists WHERE name = 'Michael Jackson'), 'Thriller', 'Pop'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 'September (Single)', 'R&B');


-- Insert Dummy Songs Data
INSERT INTO Songs (artist_id, song_title, song_genre) VALUES
((SELECT artist_id FROM Artists WHERE name = 'Michael Jackson'), 'Thriller', 'Pop'),
((SELECT artist_id FROM Artists WHERE name = 'Michael Jackson'), 'Beat It', 'Comedy'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 'September', 'R&B'),
((SELECT artist_id FROM Artists WHERE name = 'Earth, Wind & Fire'), 'Fantasy', 'R&B'),
((SELECT artist_id FROM Artists WHERE name = 'Pink Floyd'), 'Time', 'Prog. Rock'),
((SELECT artist_id FROM Artists WHERE name = 'Pink Floyd'), 'Money', 'Prog. Rock'),
((SELECT artist_id FROM Artists WHERE name = 'Chick Corea and Return to Forever'), 'Light as a Feather', 'Jazz Fusion'),
((SELECT artist_id FROM Artists WHERE name = 'Chick Corea and Return to Forever'), 'Spain', 'Jazz Fusion'),
((SELECT artist_id FROM Artists WHERE name = '"Weird Al" Yankovic'), 'Lasagna', 'Comedy'),
((SELECT artist_id FROM Artists WHERE name = '"Weird Al" Yankovic'), 'Fat', 'Comedy');


-- Insert Dummy Song_Reviews Data
INSERT INTO Song_Reviews (user_id, song_id, song_rating, song_review_body) VALUES
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT song_id FROM Songs WHERE song_title = 'Thriller'), 5, "There's a reason why Michael Jackson is known as the King of Pop!"),
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT song_id FROM Songs WHERE song_title = 'September'), 5, '"Do you remember, the 21st night of September?"'),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT song_id FROM Songs WHERE song_title = 'Spain'), 5, 'RIP Chick Corea. You truly pushed the boundaries of Jazz and created such an amazing Jazz standard.'),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT song_id FROM Songs WHERE song_title = 'September'), 5, NULL),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT song_id FROM Songs WHERE song_title = 'Money'), 5, NULL),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT song_id FROM Songs WHERE song_title = 'Fat'), 5, '"He who is tired of Weird Al is tired of life." - Homer Simpson');


-- Insert Dummy Album_Reviews Data
INSERT INTO Album_Reviews (user_id, album_id, album_rating, album_review_body) VALUES
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT album_id FROM Albums WHERE album_title = 'Thriller'), 5, "C'mon, Thriller AND Beat It are on this album! 5/5"),
((SELECT user_id FROM Users WHERE username = 'user1'), (SELECT album_id FROM Albums WHERE album_title = 'The Best of Earth, Wind & Fire Vol. 1'), 5, 'Love me some Earth, Wind & Fire.'),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT album_id FROM Albums WHERE album_title = 'Light as a Feather'), 4, "I'm a huge fan of Spain, but I don't think the entire album is a hit."),
((SELECT user_id FROM Users WHERE username = 'user2'), (SELECT album_id FROM Albums WHERE album_title = 'September (Single)'), 5, 'September was good enough as a single. Enough said.'),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT album_id FROM Albums WHERE album_title = 'The Dark Side of the Moon'), 5, 'You have to listen to the whole album at once.'),
((SELECT user_id FROM Users WHERE username = 'user3'), (SELECT album_id FROM Albums WHERE album_title = 'Even Worse'), 4, NULL);


-- Insert Dummy Albums_Songs Data
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


-- SELECT * FROM Albums;
-- SELECT * FROM Songs;
-- SELECT * FROM Artists;
-- SELECT * FROM Users;
-- SELECT * FROM Song_Reviews;
-- SELECT * FROM Album_Reviews;
-- SELECT * FROM Albums_Songs;

SET FOREIGN_KEY_CHECKS=1;
COMMIT;