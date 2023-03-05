import database.db_connector as db

##################################################
#                                                #
# REVIEW QUERIES                                 #
#                                                #
##################################################

##### ALBUM REVIEWS ######
def get_all_album_reviews():
    """ Returns aliased information about all Album_Reviews """
    return db.execute_query(("SELECT Album_Reviews.album_review_id AS 'Album Review ID', Albums.album_title AS Album, Users.username AS User, album_rating AS Rating, album_review_body AS Review FROM Album_Reviews"
                             " JOIN Users ON Users.user_id = Album_Reviews.user_id"
                             " JOIN Albums ON Albums.album_id = Album_Reviews.album_id"
                             " ORDER BY Albums.album_title ASC;")).fetchall()

def get_album_id_from_album_review_id(album_review_id) -> int:
    """ Returns the corresponding album_id for the given album_review_id """
    return int(db.execute_query(f"SELECT album_id FROM Album_Reviews WHERE album_review_id = {album_review_id}").fetchone()['album_id'])

##### SONG REVIEWS ######
def get_all_song_reviews():
    """ Returns aliased information about all Song_Reviews """
    return db.execute_query(("SELECT Song_Reviews.song_review_id AS 'Song Review ID', Songs.song_title AS Song, Users.username AS User, song_rating AS Rating, song_review_body AS Review FROM Song_Reviews"
                             " JOIN Users ON Users.user_id = Song_Reviews.user_id"
                             " JOIN Songs ON Songs.song_id = Song_Reviews.song_id"
                             " ORDER BY Songs.song_title ASC;")).fetchall()

def get_song_id_from_song_review_id(song_review_id) -> int:
    """ Returns the corresponding song_id for the given song_review_id """
    return int(db.execute_query(f"SELECT song_id FROM Song_Reviews WHERE song_review_id = {song_review_id}").fetchone()['song_id'])

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
    return db.execute_query(("SELECT Albums.album_id AS 'Album ID', Albums.album_title AS Album, Artists.name AS Artist, Albums.album_genre AS Genre, Albums.avg_album_rating AS 'Average Rating' FROM Albums"
                             " JOIN Artists ON Artists.artist_id = Albums.artist_id"
                             " ORDER BY Albums.album_title ASC;")).fetchall()

def get_album_titles():
    """ Returns all album_title values from the Albums table """
    return db.execute_query("SELECT album_title FROM Albums;").fetchall()

def get_album_id_from_title(title) -> int:
    """ Returns the album_id that corresponds to the given album_title """
    return int(db.execute_query(f"SELECT album_id FROM Albums WHERE album_title = ('{title}')").fetchone()['album_id'])

def get_album_title_from_id(album_id) -> str:
    """ Returns the album_title that corresponds to the given album_id """
    return db.execute_query(f"SELECT album_title FROM Albums WHERE album_id = {album_id}").fetchone()['album_title']

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
                             " ORDER BY Albums_Songs.albums_song_id ASC;")).fetchall()

def get_star_albums_songs():
    """ Returns all information from the Albums_Songs table, without aliases """
    return db.execute_query(f"SELECT * FROM Albums_Songs;").fetchall()

def get_albums_song_song_id(albums_song_id) -> int:
    """ Returns the song_id value of the Albums_Song with the given ID """
    return db.execute_query(f"SELECT song_id FROM Albums_Songs WHERE albums_song_id = {albums_song_id}").fetchone()['song_id']

def get_albums_song_album_id(albums_song_id) -> int:
    """ Returns the album_id value of the Albums_Song with the given ID """
    return db.execute_query(f"SELECT album_id FROM Albums_Songs WHERE albums_song_id = {albums_song_id}").fetchone()['album_id']

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
                             " ORDER BY Artists.name ASC;")).fetchall()

def get_artist_names():
    """ Returns all name values from the Artists table """
    return db.execute_query("SELECT name FROM Artists;").fetchall()

def get_artist_name_from_id(artist_id) -> str:
    """ Returns the corresponding name value for the given artist_id """
    return db.execute_query(f"SELECT name FROM Artists WHERE artist_id = {artist_id}").fetchone()['name']

def get_current_artist_id_from_table(table_name, entity_id):
    """ Returns the current artist_id value for the given table and entity ID's artist """
    return db.execute_query(f"SELECT artist_id FROM {table_name}s WHERE {table_name.lower()}_id = {entity_id}").fetchone()['artist_id']


##################################################
#                                                #
# SONG QUERIES                                   #
#                                                #
##################################################

def get_all_songs():
    """ Returns aliased information about all Songs """
    return db.execute_query(("SELECT Songs.song_id AS 'Song ID', Songs.song_title AS Song, Artists.name AS Artist, Songs.song_genre AS Genre, Songs.avg_song_rating AS 'Average Rating' FROM Songs"
                             " JOIN Artists ON Artists.artist_id = Songs.artist_id"
                             " ORDER BY Songs.song_title ASC;")).fetchall()

def get_song_titles():
    """ Returns all song_title values from the Songs table """
    return db.execute_query("SELECT song_title FROM Songs;").fetchall()

def get_song_id_from_title(title) -> int:
    """ Returns the corresponding song_id given a song_title """
    return int(db.execute_query(f"SELECT song_id FROM Songs WHERE song_title = ('{title}')").fetchone()['song_id'])

def get_song_title_from_id(song_id) -> str:
    """ Returns the corresponding song_title given a song_id """
    return db.execute_query(f"SELECT song_title FROM Songs WHERE song_id = {song_id}").fetchone()['song_title']

##################################################
#                                                #
# USER QUERIES                                   #
#                                                #
##################################################

def get_all_users():
    """ Returns aliased information about all Users """
    return db.execute_query(("SELECT Users.user_id AS 'User ID', username AS User, email AS 'E-mail' FROM Users"
                             " ORDER BY username ASC;")).fetchall()
def get_usernames():
    """ Returns all username values from the Users table """
    return db.execute_query("SELECT username FROM Users;").fetchall()

def get_username_from_user_id(user_id) -> str:
    """ Returns the corresponding username value for the given user_id """
    return db.execute_query(f"SELECT username FROM Users WHERE user_id = {user_id}").fetchone()['username']

def add_user(username, email) -> None:
    """ Inserts a new User entity with the given username and email """
    db.execute_query(f"INSERT INTO Users (username, email) VALUES ('{username}', '{email}')")

def edit_user(username, email, user_id) -> None:
    """  """
    db.execute_query(f"UPDATE Users SET username = '{username}', email = '{email}' WHERE user_id = {user_id}")

def delete_user(user_id) -> None:
    """ Deletes a User entity using its unique user_id """
    db.execute_query(f"DELETE FROM Users WHERE user_id = {user_id}")

##################################################
#                                                #
# GENERAL QUERIES                                #
#                                                #
##################################################

def get_star_entity(entity_name):
    """  """
    return db.execute_query(f"SELECT * FROM {entity_name.capitalize()}s;").fetchall()

def get_star_entity_where_id(entity_name, id):
    """ Gets all of the rows from entity_name's table where the entity's primary key ID matches id """
    return db.execute_query(f"SELECT * FROM {entity_name}s WHERE {entity_name}_id = {id}").fetchall()