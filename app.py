from flask import Flask, render_template, redirect, url_for
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)

#db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/song-reviews', methods=['GET', 'POST'])
def song_reviews():

    query = ("SELECT song_review_id, Songs.song_title AS Song, Users.username AS User, song_rating AS Rating, song_review_body AS Review FROM Song_Reviews"
             " JOIN Users ON Users.user_id = Song_Reviews.user_id"
             " JOIN Songs ON Songs.song_id = Song_Reviews.song_id"
             " ORDER BY Songs.song_title ASC;")
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("entities/song_reviews.html", song_reviews=results)

@app.route('/album-reviews', methods=['GET', 'POST'])
def album_reviews():

    query = ("SELECT album_review_id, Albums.album_title AS Album, Users.username AS User, album_rating AS Rating, album_review_body AS Review FROM Album_Reviews"
             " JOIN Users ON Users.user_id = Album_Reviews.user_id"
             " JOIN Albums ON Albums.album_id = Album_Reviews.album_id"
             " ORDER BY Albums.album_title ASC;")
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("entities/album_reviews.html", album_reviews=results)

@app.route('/songs', methods=['GET', 'POST'])
def songs():

    query = ("SELECT song_id, Songs.song_title AS Song, Artists.name AS Artist, Songs.song_genre AS Genre, Songs.avg_song_rating AS 'Average Rating' FROM Songs"
             " JOIN Artists ON Artists.artist_id = Songs.artist_id"
             " ORDER BY Songs.song_title ASC;")
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("entities/songs.html", songs=results)

@app.route('/albums', methods=['GET', 'POST'])
def albums():

    query = ("SELECT album_id, Albums.album_title AS Album, Artists.name AS Artist, Albums.album_genre AS Genre, Albums.avg_album_rating AS 'Average Rating' FROM Albums"
             " JOIN Artists ON Artists.artist_id = Albums.artist_id"
             " ORDER BY Albums.album_title ASC;")
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("entities/albums.html", albums=results)

@app.route('/albums-songs', methods=['GET', 'POST'])
def albums_songs():

    query = ("SELECT Albums_Songs.albums_song_id AS 'Album Song ID', Albums.album_title AS Album, Songs.song_title AS Song FROM Albums_Songs"
             " LEFT JOIN Albums ON Albums.album_id = Albums_Songs.album_id"
             " LEFT JOIN Songs ON Songs.song_id = Albums_Songs.song_id"
             " ORDER BY Albums_Songs.albums_song_id ASC;")
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("entities/albums_songs.html", albums_songs=results)

@app.route('/artists', methods=['GET', 'POST'])
def artists():

    query = ("SELECT artist_id, Artists.name AS Artist FROM Artists"
             " ORDER BY Artists.name ASC;")
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("entities/artists.html", artists=results)

@app.route('/users', methods=['GET', 'POST'])
def users():

    query = ("SELECT user_id, username AS User, email AS 'E-mail' FROM Users"
             " ORDER BY username ASC;")
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("entities/users.html", users=results)

@app.route('/add/<review_type>-review', methods=['GET', 'POST'])
def add_review(review_type):

    query = f"SELECT {review_type}_title FROM {review_type.capitalize()}s;"
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("add_review.html", media_type=review_type, media_list=results)

@app.route('/add/<entity_name>', methods=['GET', 'POST'])
def add_entity(entity_name):

    if entity_name == "albums_song":
        entity_name = "Albums_Song"
    else:
        entity_name = entity_name.capitalize()

    query = f"SELECT * FROM {entity_name}s;"
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    if entity_name == "Song":
        artist_results = db.execute_query("SELECT name FROM Artists;").fetchall()
        album_results = db.execute_query("SELECT album_title FROM Albums;").fetchall()
        return render_template("add_entity.html", entity_results=results, artist_fk_data=artist_results, album_fk_data=album_results, entity_name=entity_name.lower())
    elif entity_name == "Albums_Song":
        song_results = db.execute_query("SELECT song_title FROM Songs;").fetchall()
        album_results = db.execute_query("SELECT album_title FROM Albums;").fetchall()
        return render_template("add_entity.html", entity_results=results, artist_fk_data=song_results, album_fk_data=album_results, entity_name=entity_name.lower())
    elif entity_name == "Album":
        artist_results = db.execute_query("SELECT name FROM Artists;").fetchall()
        return render_template("add_entity.html", entity_results=results, artist_fk_data=artist_results, album_fk_data=[], entity_name=entity_name.lower())
    else:
        return render_template("add_entity.html", entity_results=results, artist_fk_data=[], album_fk_data=[], entity_name=entity_name.lower())

@app.route('/edit/<entity_name>/<entity_id>', methods=['GET', 'POST'])
def edit(entity_name, entity_id):

    if entity_name == "album_review":
        entity_name = "Album_Review"
    elif entity_name == "song_review":
        entity_name = "Song_Review"
    else:
        entity_name = entity_name.capitalize()

    if entity_name == "Albums_songs":
        query = f"SELECT * FROM Albums_Songs WHERE albums_song_id = {entity_id};"
        entity_name = "Albums_Song"
    else:
        query = f"SELECT * FROM {entity_name}s WHERE {entity_name.lower()}_id = {entity_id};"
    cursor = db.execute_query(query=query)
    results = cursor.fetchall()

    return render_template("edit.html", entity_results=results, entity_name=entity_name)


@app.route('/delete/<entity_name>', methods=['GET', 'POST'])
def delete(entity_name):

    print(f"Deleting a {entity_name.capitalize()}")

    return redirect(url_for(entity_name.lower() + 's'))

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 58767)) 
    app.run(port=port, debug=True) 