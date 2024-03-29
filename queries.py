import database.db_connector as db

##################################################
#                                                #
# REVIEW QUERIES                                 #
#                                                #
##################################################

##### ALBUM REVIEWS ######
def get_all_album_reviews():
    """ Returns aliased information about all Album_Reviews """
    return db.execute_query(("SELECT Album_Reviews.album_review_id AS 'Album Review ID', Albums.album_title AS Album, Users.username AS User, album_rating AS Rating, IF(album_review_body='' OR IFNULL(album_review_body, 'NULL')='NULL', 'N/A', album_review_body) AS Review FROM Album_Reviews"
                             " JOIN Users ON Users.user_id = Album_Reviews.user_id"
                             " JOIN Albums ON Albums.album_id = Album_Reviews.album_id"
                             " UNION ALL"
                             " SELECT Album_Reviews.album_review_id AS 'Album Review ID', Albums.album_title AS Album, IFNULL(Album_Reviews.user_id, 'N/A') AS User, album_rating AS Rating, IF(album_review_body='' OR IFNULL(album_review_body, 'NULL')='NULL', 'N/A', album_review_body) AS Review FROM Album_Reviews"
                             " JOIN Albums ON Albums.album_id = Album_Reviews.album_id"
                             " WHERE (SELECT ISNULL(Album_Reviews.user_id)) = 1"
                             " ORDER BY `Album Review ID` ASC;")).fetchall()

def get_album_id_from_album_review_id(album_review_id) -> int:
    """ Returns the corresponding album_id for the given album_review_id """
    return int(db.execute_query(f"SELECT album_id FROM Album_Reviews WHERE album_review_id = {album_review_id}").fetchone()['album_id'])

def add_album_review_with_user(user_id, album_id, album_rating, album_review_body) -> None:
    """ Inserts a new Album_Review entity with the given user_id, album_id, album_rating, and album_review_body """
    db.execute_query(f"INSERT INTO Album_Reviews (user_id, album_id, album_rating, album_review_body) VALUES ({user_id}, {album_id}, (%s), (%s))", (album_rating, album_review_body))
    update_album_rating(album_id)

def add_album_review_without_user(album_id, album_rating, album_review_body) -> None:
    """ Inserts a new Album_Review entity with the given album_id, album_rating, and album_review_body """
    db.execute_query(f"INSERT INTO Album_Reviews (album_id, album_rating, album_review_body) VALUES ({album_id}, (%s), (%s))", (album_rating, album_review_body))
    update_album_rating(album_id)

def edit_album_review_with_user(user_id, album_id, album_rating, album_review_body, album_review_id) -> None:
    """ Updates an existing Album_Review entity with the given user_id, album_id, album_rating, and album_review_body """
    db.execute_query(f"UPDATE Album_Reviews SET user_id = (%s), album_id = (%s), album_rating = (%s), album_review_body = (%s) WHERE album_review_id = {album_review_id}", (user_id, album_id, album_rating, album_review_body))
    update_album_rating(album_id)

def edit_album_review_without_user(album_id, album_rating, album_review_body, album_review_id) -> None:
    """ Updates an existing Album_Review entity with the given album_id, album_rating, and album_review_body """
    db.execute_query(f"UPDATE Album_Reviews SET user_id = NULL, album_id = (%s), album_rating = (%s), album_review_body = (%s) WHERE album_review_id = {album_review_id}", (album_id, album_rating, album_review_body))
    update_album_rating(album_id)

def delete_album_review(album_review_id) -> None:
    """ Deletes an Album_Review entity using its unique album_review_id """
    album_id = get_album_id_from_album_review_id(album_review_id)
    db.execute_query(f"DELETE FROM Album_Reviews WHERE album_review_id = {album_review_id}")
    update_album_rating(album_id)

def update_album_rating(album_id) -> None:
    """
    Updates an album's avg_album_rating value based on all Album_Review entries for the Album with the given album_id.
    Used in place of a MySQL trigger function.
    """
    db.execute_query("UPDATE Albums SET avg_album_rating = ("
                    " SELECT AVG(album_rating) FROM Album_Reviews"
                    f" WHERE Album_Reviews.album_id = {album_id}"
                    " )"
                    f" WHERE Albums.album_id = {album_id};") 

##### SONG REVIEWS ######
def get_all_song_reviews():
    """ Returns aliased information about all Song_Reviews """
    return db.execute_query(("SELECT * FROM ("
                             " SELECT Song_Reviews.song_review_id AS 'Song Review ID', Songs.song_title AS Song, Users.username AS User, song_rating AS Rating, IF(song_review_body='' OR IFNULL(song_review_body, 'NULL')='NULL', 'N/A', song_review_body) AS Review FROM Song_Reviews"
                             " JOIN Users ON Users.user_id = Song_Reviews.user_id"
                             " JOIN Songs ON Songs.song_id = Song_Reviews.song_id"
                             " UNION ALL"
                             " SELECT Song_Reviews.song_review_id AS 'Song Review ID', Songs.song_title AS Song, IFNULL(Song_Reviews.user_id, 'N/A') AS User, song_rating AS Rating, IF(song_review_body='' OR IFNULL(song_review_body, 'NULL')='NULL', 'N/A', song_review_body) AS Review FROM Song_Reviews"
                             " JOIN Songs ON Songs.song_id = Song_Reviews.song_id"
                             " WHERE (SELECT ISNULL(Song_Reviews.user_id)) = 1) AS a"
                             " ORDER BY `Song Review ID` ASC;")).fetchall()

def get_song_id_from_song_review_id(song_review_id) -> int:
    """ Returns the corresponding song_id for the given song_review_id """
    return int(db.execute_query(f"SELECT song_id FROM Song_Reviews WHERE song_review_id = {song_review_id}").fetchone()['song_id'])

def add_song_review_with_user(user_id, song_id, song_rating, song_review_body) -> None:
    """ Inserts a new Song_Reviews entity with the given user_id, song_id, song_rating, and song_review_body """
    db.execute_query(f"INSERT INTO Song_Reviews (user_id, song_id, song_rating, song_review_body) VALUES ({user_id}, {song_id}, (%s), (%s))", (song_rating, song_review_body))
    update_song_rating(song_id)

def add_song_review_without_user(song_id, song_rating, song_review_body) -> None:
    """ Inserts a new Song_Reviews entity with the given song_id, song_rating, and song_review_body """
    db.execute_query(f"INSERT INTO Song_Reviews (song_id, song_rating, song_review_body) VALUES ({song_id}, (%s), (%s))", (song_rating, song_review_body))
    update_song_rating(song_id)

def edit_song_review_with_user(user_id, song_id, song_rating, song_review_body, song_review_id) -> None:
    """ Updates an existing Song_Review entity with the given user_id, song_id, song_rating, and song_review_body """
    db.execute_query(f"UPDATE Song_Reviews SET user_id = (%s), song_id = (%s), song_rating = (%s), song_review_body = (%s) WHERE song_review_id = {song_review_id}", (user_id, song_id, song_rating, song_review_body))
    update_song_rating(song_id)

def edit_song_review_without_user(song_id, song_rating, song_review_body, song_review_id) -> None:
    """ Updates an existing Song_Review entity with the given song_id, song_rating, and song_review_body """
    db.execute_query(f"UPDATE Song_Reviews SET user_id = NULL, song_id = (%s), song_rating = (%s), song_review_body = (%s) WHERE song_review_id = {song_review_id}", (song_id, song_rating, song_review_body))
    update_song_rating(song_id)

def delete_song_review(song_review_id) -> None:
    """ Deletes an Song_Review entity using its unique song_review_id """
    song_id = get_song_id_from_song_review_id(song_review_id)
    db.execute_query(f"DELETE FROM Song_Reviews WHERE song_review_id = {song_review_id}")
    update_song_rating(song_id)

def update_song_rating(song_id) -> None:
    """
    Updates a song's avg_song_rating value based on all Song_Review entries for the Song with the given song_id.
    Used in place of a MySQL trigger function.
    """
    db.execute_query("UPDATE Songs SET avg_song_rating = ("
                     " SELECT AVG(song_rating) FROM Song_Reviews"
                    f" WHERE Song_Reviews.song_id = {song_id})"
                    f" WHERE Songs.song_id = {song_id};")

##### BOTH REVIEWS #####
def get_add_review_info(review_type) -> tuple:
    """
    Returns all album/song titles (depending on review_type) and usernames as a tuple,
        where titles are stored at the 0th index and usernames are stored at the 1st index
    """
    reviews = db.execute_query(f"SELECT {review_type}_title FROM {review_type.capitalize()}s;").fetchall()
    users = db.execute_query("SELECT username FROM Users")

    return (reviews, users)

def get_user_id_from_review_id(review_type, review_id):
    """ Returns the user_id for the given review's ID """
    return db.execute_query(f"SELECT user_id FROM {review_type}s WHERE {review_type.lower()}_id = {review_id}").fetchone()['user_id']


##################################################
#                                                #
# ALBUM QUERIES                                  #
#                                                #
##################################################

def get_all_albums():
    """ Returns aliased information about all Albums """
    return db.execute_query(("SELECT Albums.album_id AS 'Album ID', Albums.album_title AS Album, Artists.name AS Artist, Albums.album_genre AS Genre, IF(Albums.avg_album_rating = 0.0, 'N/A', Albums.avg_album_rating) AS 'Average Rating' FROM Albums"
                             " JOIN Artists ON Artists.artist_id = Albums.artist_id"
                             " ORDER BY `Album ID` ASC;")).fetchall()

def get_album_titles():
    """ Returns all album_title values from the Albums table """
    return db.execute_query("SELECT album_title FROM Albums;").fetchall()

def get_album_id_from_title(title) -> int:
    """ Returns the album_id that corresponds to the given album_title """
    return int(db.execute_query(f"SELECT album_id FROM Albums WHERE album_title = ((%s))", (title,)).fetchone()['album_id'])

def get_album_title_from_id(album_id) -> str:
    """ Returns the album_title that corresponds to the given album_id """
    return db.execute_query(f"SELECT album_title FROM Albums WHERE album_id = {album_id}").fetchone()['album_title']

def add_album(artist_id, album_title, album_genre) -> None:
    """ Inserts a new Album entity with the given artist_id, album_title, and album_genre """
    db.execute_query(f"INSERT INTO Albums (artist_id, album_title, album_genre) VALUES ('{artist_id}', (%s), (%s))", (album_title, album_genre))

def edit_album(artist_id, album_title, album_genre, album_id) -> None:
    """ Updates the artist_id, album_title, and album_genre of the Album with the given album_id """
    db.execute_query(f"UPDATE Albums SET artist_id = '{artist_id}', album_title = (%s), album_genre = (%s) WHERE album_id = {album_id}", (album_title, album_genre))

def delete_album(album_id) -> None:
    """ Deletes an Album entity using its unique album_id """
    db.execute_query(f"DELETE FROM Albums WHERE album_id = {album_id}")

##################################################
#                                                #
# ALBUMS_SONGS QUERIES                           #
#                                                #
##################################################

def get_all_albums_songs():
    """ Returns aliased information about all Albums_Songs """
    return db.execute_query(("SELECT Albums_Songs.albums_song_id AS 'Album Song ID', Albums.album_title AS Album, Songs.song_title AS Song FROM Albums_Songs"
                             " LEFT JOIN Albums ON Albums.album_id = Albums_Songs.album_id"
                             " LEFT JOIN Songs ON Songs.song_id = Albums_Songs.song_id"
                             " ORDER BY `Album Song ID` ASC;")).fetchall()

def get_star_albums_songs():
    """ Returns all information from the Albums_Songs table, without aliases """
    return db.execute_query(f"SELECT * FROM Albums_Songs;").fetchall()

def get_albums_songs_columns():
    """ Returns the names of all of the columns in the Albums_Songs table """
    return tuple(column['Field'] for column in db.execute_query("DESCRIBE Albums_Songs;").fetchall())

def get_albums_song_song_id(albums_song_id) -> int:
    """ Returns the song_id value of the Albums_Song with the given ID """
    return db.execute_query(f"SELECT song_id FROM Albums_Songs WHERE albums_song_id = {albums_song_id}").fetchone()['song_id']

def get_albums_song_album_id(albums_song_id) -> int:
    """ Returns the album_id value of the Albums_Song with the given ID """
    return db.execute_query(f"SELECT album_id FROM Albums_Songs WHERE albums_song_id = {albums_song_id}").fetchone()['album_id']

def get_albums_song_data_from_id(albums_song_id) -> int:
    """ Returns the album_id and song_id values of the Albums_Song with the given ID """
    return db.execute_query(f"SELECT * FROM Albums_Songs WHERE albums_song_id = {albums_song_id}").fetchone()

def add_albums_song(album_id, song_id) -> None:
    """ Inserts a new Albums_Songs entity with the given album_id and song_id """
    db.execute_query(f"INSERT INTO Albums_Songs (album_id, song_id) VALUES ('{album_id}', '{song_id}')")

def edit_albums_song(album_id, song_id, albums_song_id) -> None:
    """  """
    db.execute_query(f"UPDATE Albums_Songs SET album_id = {album_id}, song_id = {song_id} WHERE albums_song_id = {albums_song_id}")

def delete_albums_song(albums_song_id) -> None:
    """ Deletes an Albums_Songs entity using its unique albums_song_id """
    db.execute_query(f"DELETE FROM Albums_Songs WHERE albums_song_id = {albums_song_id}")

def check_albums_song_exists(album_id, song_id) -> int:
    """
    Checks if an Albums_Song with the given album_id and song_id already exists.
    Returns 0 if it does not exist, and returns 1 if it does exist.
    """
    query = f"SELECT EXISTS(SELECT * FROM Albums_Songs WHERE album_id = {album_id} AND song_id = {song_id})"
    return list((db.execute_query(query).fetchone()).values())[0]

##################################################
#                                                #
# ARTISTS QUERIES                                #
#                                                #
##################################################

def get_all_artists():
    """ Returns aliased information about all Artists """
    return db.execute_query(("SELECT Artists.artist_id AS 'Artist ID', Artists.name AS Artist FROM Artists"
                             " ORDER BY `Artist ID` ASC;")).fetchall()

def get_artist_names():
    """ Returns all name values from the Artists table """
    return db.execute_query("SELECT name FROM Artists;").fetchall()

def get_artist_id_from_name(name) -> int:
    """ Returns the corresponding artist_id given a name """
    return int(db.execute_query(f"SELECT artist_id FROM Artists WHERE name = ((%s))", (name,)).fetchone()['artist_id'])

def get_artist_name_from_id(artist_id) -> str:
    """ Returns the corresponding name value for the given artist_id """
    return db.execute_query(f"SELECT name FROM Artists WHERE artist_id = {artist_id}").fetchone()['name']

def get_current_artist_id_from_table(table_name, entity_id):
    """ Returns the current artist_id value for the given table and entity ID's artist """
    return db.execute_query(f"SELECT artist_id FROM {table_name}s WHERE {table_name.lower()}_id = {entity_id}").fetchone()['artist_id']

def add_artist(name) -> None:
    """ Inserts a new Artist entity with the given name """
    db.execute_query(f"INSERT INTO Artists (name) VALUES ((%s))", (name,))

def edit_artist(name, artist_id) -> None:
    """ Updates the name of the Artist with the given artist_id """
    db.execute_query(f"UPDATE Artists SET name = (%s) WHERE artist_id = {artist_id}", (name,))

def delete_artist(artist_id) -> None:
    """ Deletes an Artist entity using its unique artist_id """
    db.execute_query("SET foreign_key_checks = 0;")
    db.execute_query(f"DELETE FROM Artists WHERE artist_id = {artist_id}")

def check_artist_exists(name) -> int:
    """
    Checks if an Artist with the given name already exists.
    Returns 0 if it does not exist, and returns 1 if it does exist.
    """
    query = f"SELECT EXISTS(SELECT * FROM Artists WHERE name = (%s))"
    return list((db.execute_query(query, (name,)).fetchone()).values())[0]

##################################################
#                                                #
# SONG QUERIES                                   #
#                                                #
##################################################

def get_all_songs():
    """ Returns aliased information about all Songs """
    return db.execute_query(("SELECT Songs.song_id AS 'Song ID', Songs.song_title AS Song, Artists.name AS Artist, Songs.song_genre AS Genre, IF(Songs.avg_song_rating = 0.0, 'N/A', Songs.avg_song_rating) AS 'Average Rating' FROM Songs"
                             " JOIN Artists ON Artists.artist_id = Songs.artist_id"
                             " ORDER BY `Song ID` ASC;")).fetchall()

def get_song_titles():
    """ Returns all song_title values from the Songs table """
    return db.execute_query("SELECT song_title FROM Songs;").fetchall()

def get_song_id_from_title(title) -> int:
    """ Returns the corresponding song_id given a song_title """
    return int(db.execute_query(f"SELECT song_id FROM Songs WHERE song_title = (%s)", (title,)).fetchone()['song_id'])

def get_song_title_from_id(song_id) -> str:
    """ Returns the corresponding song_title given a song_id """
    return db.execute_query(f"SELECT song_title FROM Songs WHERE song_id = {song_id}").fetchone()['song_title']

def get_song_id_from_title_and_artist(title, artist_id) -> int:
    """ Returns the corresponding song_id given a song_title and artist"""
    return int(db.execute_query(f"SELECT song_id FROM Songs WHERE song_title = (%s) AND artist_id = '{artist_id}'", (title,)).fetchone()['song_id'])

def add_song(artist_id, song_title, song_genre) -> None:
    """ Inserts a new Song entity with the given artist_id, song_title, and song_genre """
    db.execute_query(f"INSERT INTO Songs (artist_id, song_title, song_genre) VALUES ('{artist_id}', (%s), (%s))", (song_title, song_genre))

def edit_song(artist_id, song_title, song_genre, song_id) -> None:
    """ Updates the artist_id, song_title, and song_genre of the Song with the given song_id """
    db.execute_query(f"UPDATE Songs SET artist_id = '{artist_id}', song_title = (%s), song_genre = (%s) WHERE song_id = {song_id}", (song_title, song_genre))

def delete_song(song_id) -> None:
    """ Deletes a Song entity using its unique song_id """
    db.execute_query(f"DELETE FROM Songs WHERE song_id = {song_id}")

##################################################
#                                                #
# USER QUERIES                                   #
#                                                #
##################################################

def get_all_users():
    """ Returns aliased information about all Users """
    return db.execute_query(("SELECT Users.user_id AS 'User ID', username AS Username, email AS 'E-mail' FROM Users"
                             " ORDER BY `User ID` ASC;")).fetchall()
def get_usernames():
    """ Returns all username values from the Users table """
    return db.execute_query("SELECT username FROM Users;").fetchall()

def get_username_from_user_id(user_id) -> str:
    """ Returns the corresponding username value for the given user_id """
    if user_id is None:
        return "None"

    return db.execute_query(f"SELECT username FROM Users WHERE user_id = {user_id}").fetchone()['username']

def get_email_from_user_id(user_id) -> str:
    """ Returns the corresponding email value for the given user_id """
    return db.execute_query(f"SELECT email FROM Users WHERE user_id = {user_id}").fetchone()['email']

def get_user_id_from_username(username) -> int:
    """ Returns the corresponding user_id value for the given username """
    return int(db.execute_query(f"SELECT user_id FROM Users WHERE username = (%s)", (username,)).fetchone()['user_id'])

def add_user(username, email) -> None:
    """ Inserts a new User entity with the given username and email """
    db.execute_query(f"INSERT INTO Users (username, email) VALUES ((%s), (%s))", (username, email))

def edit_user(username, email, user_id) -> None:
    """ Updates the username and email of the User with the given user_id """
    db.execute_query(f"UPDATE Users SET username = (%s), email = (%s) WHERE user_id = {user_id}", (username, email))

def delete_user(user_id) -> None:
    """ Deletes a User entity using its unique user_id """
    db.execute_query(f"DELETE FROM Users WHERE user_id = {user_id}")

def check_user_username_exists(username) -> int:
    """
    Checks if a User with the given username already exists.
    Returns 0 if it does not exist, and returns 1 if it does exist.
    """
    query = f"SELECT EXISTS(SELECT * FROM Users WHERE username = (%s))"
    return list((db.execute_query(query, (username,)).fetchone()).values())[0]

def check_user_email_exists(email) -> int:
    """
    Checks if a User with the given email already exists.
    Returns 0 if it does not exist, and returns 1 if it does exist.
    """
    query = f"SELECT EXISTS(SELECT * FROM Users WHERE email = (%s))"
    return list((db.execute_query(query, (email,)).fetchone()).values())[0]

##################################################
#                                                #
# GENERAL QUERIES                                #
#                                                #
##################################################

def get_star_entity(entity_name):
    """  """
    return db.execute_query(f"SELECT * FROM {entity_name.capitalize()}s;").fetchall()

def get_entity_columns(entity_name) -> tuple:
    """ Returns the names of all of the columns in the given entity's table """
    return tuple(column['Field'] for column in db.execute_query(f"DESCRIBE {entity_name.capitalize()}s").fetchall())

def get_star_entity_where_id(entity_name, id):
    """ Gets all of the rows from entity_name's table where the entity's primary key ID matches id """
    return db.execute_query(f"SELECT * FROM {entity_name}s WHERE {entity_name}_id = {id}").fetchall()