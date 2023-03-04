import database.db_connector as db

def get_all_album_reviews():
    """ Returns all rows from the Album_Reviews table. """
    return db.execute_query(("SELECT Album_Reviews.album_review_id AS 'Album Review ID', Albums.album_title AS Album, Users.username AS User, album_rating AS Rating, album_review_body AS Review FROM Album_Reviews"
                             " JOIN Users ON Users.user_id = Album_Reviews.user_id"
                             " JOIN Albums ON Albums.album_id = Album_Reviews.album_id"
                             " ORDER BY Albums.album_title ASC;")).fetchall()

def get_all_song_reviews():
    """ Returns all rows from the Song_Reviews table. """
    return db.execute_query(("SELECT Song_Reviews.song_review_id AS 'Song Review ID', Songs.song_title AS Song, Users.username AS User, song_rating AS Rating, song_review_body AS Review FROM Song_Reviews"
                             " JOIN Users ON Users.user_id = Song_Reviews.user_id"
                             " JOIN Songs ON Songs.song_id = Song_Reviews.song_id"
                             " ORDER BY Songs.song_title ASC;")).fetchall()

def get_all_albums():
    """  """
    return db.execute_query(("SELECT Albums.album_id AS 'Album ID', Albums.album_title AS Album, Artists.name AS Artist, Albums.album_genre AS Genre, Albums.avg_album_rating AS 'Average Rating' FROM Albums"
                             " JOIN Artists ON Artists.artist_id = Albums.artist_id"
                             " ORDER BY Albums.album_title ASC;")).fetchall()

def get_album_titles():
    """  """
    return db.execute_query("SELECT album_title FROM Albums;").fetchall()

def get_all_albums_songs():
    """  """
    return db.execute_query(("SELECT Albums_Songs.albums_song_id AS 'Album Song ID', Albums.album_title AS Album, Songs.song_title AS Song FROM Albums_Songs"
                             " LEFT JOIN Albums ON Albums.album_id = Albums_Songs.album_id"
                             " LEFT JOIN Songs ON Songs.song_id = Albums_Songs.song_id"
                             " ORDER BY Albums_Songs.albums_song_id ASC;")).fetchall()

def get_star_albums_songs():
    """  """
    return db.execute_query(f"SELECT * FROM Albums_Songs;").fetchall()

def get_all_artists():
    """  """
    return db.execute_query(("SELECT Artists.artist_id AS 'Artist ID', Artists.name AS Artist FROM Artists"
                             " ORDER BY Artists.name ASC;")).fetchall()

def get_artist_names():
    """  """
    return db.execute_query("SELECT name FROM Artists;").fetchall()

def get_all_songs():
    """  """
    return db.execute_query(("SELECT Songs.song_id AS 'Song ID', Songs.song_title AS Song, Artists.name AS Artist, Songs.song_genre AS Genre, Songs.avg_song_rating AS 'Average Rating' FROM Songs"
                             " JOIN Artists ON Artists.artist_id = Songs.artist_id"
                             " ORDER BY Songs.song_title ASC;")).fetchall()

def get_song_titles():
    """  """
    return db.execute_query("SELECT song_title FROM Songs;").fetchall()

def get_all_users():
    """  """
    return db.execute_query(("SELECT Users.user_id AS 'User ID', username AS User, email AS 'E-mail' FROM Users"
                             " ORDER BY username ASC;")).fetchall()

def get_add_review_info(review_type):
    """  """
    reviews = db.execute_query(f"SELECT {review_type}_title FROM {review_type.capitalize()}s;").fetchall()
    users = db.execute_query("SELECT username FROM Users")

    return (reviews, users)

def get_star_entity(entity_name):
    """  """
    return db.execute_query(f"SELECT * FROM {entity_name.capitalize()}s;").fetchall()