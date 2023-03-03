from flask import Flask, render_template, redirect, url_for, request, flash
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Routes
@app.route('/')
def root():
    return render_template("index.html")

@app.route('/song-reviews', methods=['GET', 'POST'])
def song_reviews():
    """ Displays the Song_Reviews table """

    results = db.execute_query(("SELECT Song_Reviews.song_review_id AS 'Song Review ID', Songs.song_title AS Song, Users.username AS User, song_rating AS Rating, song_review_body AS Review FROM Song_Reviews"
                                " JOIN Users ON Users.user_id = Song_Reviews.user_id"
                                " JOIN Songs ON Songs.song_id = Song_Reviews.song_id"
                                " ORDER BY Songs.song_title ASC;")).fetchall()

    return render_template("entities/song_reviews.html", song_reviews=results)

@app.route('/album-reviews', methods=['GET', 'POST'])
def album_reviews():
    """ Displays the Album_Reviews table """

    results = db.execute_query(("SELECT Album_Reviews.album_review_id AS 'Album Review ID', Albums.album_title AS Album, Users.username AS User, album_rating AS Rating, album_review_body AS Review FROM Album_Reviews"
                                " JOIN Users ON Users.user_id = Album_Reviews.user_id"
                                " JOIN Albums ON Albums.album_id = Album_Reviews.album_id"
                                " ORDER BY Albums.album_title ASC;")).fetchall()

    return render_template("entities/album_reviews.html", album_reviews=results)

@app.route('/songs', methods=['GET', 'POST'])
def songs():
    """ Displays the Songs table """

    results = db.execute_query(("SELECT Songs.song_id AS 'Song ID', Songs.song_title AS Song, Artists.name AS Artist, Songs.song_genre AS Genre, Songs.avg_song_rating AS 'Average Rating' FROM Songs"
                               " JOIN Artists ON Artists.artist_id = Songs.artist_id"
                               " ORDER BY Songs.song_title ASC;")).fetchall()

    return render_template("entities/songs.html", songs=results)

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    """ Displays the Albums table """

    results = db.execute_query(("SELECT Albums.album_id AS 'Album ID', Albums.album_title AS Album, Artists.name AS Artist, Albums.album_genre AS Genre, Albums.avg_album_rating AS 'Average Rating' FROM Albums"
                                " JOIN Artists ON Artists.artist_id = Albums.artist_id"
                                " ORDER BY Albums.album_title ASC;")).fetchall()

    return render_template("entities/albums.html", albums=results)

@app.route('/albums-songs', methods=['GET', 'POST'])
def albums_songs():
    """ Displays the Albums_Songs table """

    results = db.execute_query(("SELECT Albums_Songs.albums_song_id AS 'Album Song ID', Albums.album_title AS Album, Songs.song_title AS Song FROM Albums_Songs"
                               " LEFT JOIN Albums ON Albums.album_id = Albums_Songs.album_id"
                               " LEFT JOIN Songs ON Songs.song_id = Albums_Songs.song_id"
                               " ORDER BY Albums_Songs.albums_song_id ASC;")).fetchall()

    return render_template("entities/albums_songs.html", albums_songs=results)

@app.route('/artists', methods=['GET', 'POST'])
def artists():
    """ Displays the Artists table """

    results = db.execute_query(("SELECT Artists.artist_id AS 'Artist ID', Artists.name AS Artist FROM Artists"
                               " ORDER BY Artists.name ASC;")).fetchall()
    
    return render_template("entities/artists.html", artists=results)

@app.route('/users', methods=['GET', 'POST'])
def users():
    """ Displays the Users table """

    results = db.execute_query(("SELECT Users.user_id AS 'User ID', username AS User, email AS 'E-mail' FROM Users"
                                " ORDER BY username ASC;")).fetchall()

    return render_template("entities/users.html", users=results)

@app.route('/add/<review_type>-review', methods=['GET', 'POST'])
def add_review(review_type):
    """ Handles creations of Song_Reviews and Album_Reviews """

    results = db.execute_query(f"SELECT {review_type}_title FROM {review_type.capitalize()}s;").fetchall()
    users = db.execute_query("SELECT username FROM Users")

    if request.method == "POST":
        return redirect(url_for(review_type.lower() + "_reviews"))

    return render_template("add_review.html", media_type=review_type, media_list=results, users=users)

@app.route('/add/<entity_name>', methods=['GET', 'POST'])
def add_entity(entity_name):
    """ Handles creations of Songs, Albums, Artists, Users, and Albums_Songs """

    # This if-statement section is adapted from the official Flask tutorial (https://flask.palletsprojects.com/en/2.2.x/tutorial/)
    if request.method == "POST":
        if entity_name == "user":
            db.execute_query('INSERT INTO Users (username, email) VALUES (%s, %s)', (request.form['username'], request.form['email']))
            return redirect(url_for("users"))
        
        elif entity_name == "albums_song":
            album_id = int(db.execute_query('SELECT album_id FROM Albums WHERE album_title = (%s)', (request.form['album_fk_data'],)).fetchone()['album_id'])
            song_id = int(db.execute_query('SELECT song_id FROM Songs WHERE song_title = (%s)', (request.form['song_fk_data'],)).fetchone()['song_id'])

            # Check if the entry already exists, since Albums_Songs additions must be unique
            exist_val = list((db.execute_query('SELECT EXISTS(SELECT * FROM Albums_Songs WHERE album_id = ' + str(album_id) + ' AND song_id = ' + str(song_id) + ')').fetchone()).values())[0]
            print(exist_val)
            if exist_val == 1:
                flash("This Albums_Song already exists.")
                return redirect(url_for("add_entity", entity_name=entity_name))
            else:
                db.execute_query('INSERT INTO Albums_Songs (album_id, song_id) VALUES (%s, %s)', (int(album_id), int(song_id)))
                return redirect(url_for("albums_songs"))
    
    # Handle GET requests (loading page)
    elif request.method == "GET":
        if entity_name == "albums_song":
            entity_name = "Albums_Song"
        else:
            entity_name = entity_name.capitalize()

        results = db.execute_query(f"SELECT * FROM {entity_name}s;").fetchall()

        if entity_name == "Song" or entity_name == "Album":
            artist_results = db.execute_query("SELECT name FROM Artists;").fetchall()
            return render_template("add_entity.html", entity_results=results, artist_fk_data=artist_results, album_fk_data=[], entity_name=entity_name.lower())
        elif entity_name == "Albums_Song":
            song_results = db.execute_query("SELECT song_title FROM Songs;").fetchall()
            album_results = db.execute_query("SELECT album_title FROM Albums;").fetchall()
            return render_template("add_entity.html", entity_results=results, artist_fk_data=song_results, album_fk_data=album_results, entity_name=entity_name.lower())
        else:
            return render_template("add_entity.html", entity_results=results, artist_fk_data=[], album_fk_data=[], entity_name=entity_name.lower())

@app.route('/edit/<entity_name>/<int:entity_id>', methods=('GET', 'POST'))
def edit(entity_name, entity_id):
    """ Handles updates to any entity in any of the tables """

    # This if-statement section is adapted from the official Flask tutorial (https://flask.palletsprojects.com/en/2.2.x/tutorial/)
    if request.method == "POST":
        if entity_name == "user":
            db.execute_query(f'UPDATE Users SET username = %s, email = %s WHERE user_id = %s', (request.form['username'], request.form['email'], entity_id))
            return redirect(url_for("users"))

        elif entity_name == "albums_song":
            album_id = db.execute_query('SELECT album_id FROM Albums WHERE album_title = (%s)', (request.form['album_fk_data'],)).fetchone()['album_id']
            song_id = db.execute_query('SELECT song_id FROM Songs WHERE song_title = (%s)', (request.form['song_fk_data'],)).fetchone()['song_id']
            db.execute_query(f'UPDATE Albums_Songs SET album_id = %s, song_id = %s WHERE albums_song_id = %s', (album_id, song_id, entity_id))
            return redirect(url_for("albums_songs"))
        
        else:
            return redirect(url_for(entity_name + "s"))

    # Handle GET requests (loading page)
    elif request.method == "GET":
        print(entity_name)
        # TODO: Refactor below since it is reused in add_entity path
        if entity_name == "albums_song":
            entity_name = "Albums_Song"
        elif entity_name == "song_review":
            entity_name = "Song_Review"
        elif entity_name == "album_review":
            entity_name = "Album_Review"
        else:
            entity_name = entity_name.capitalize()

        results = db.execute_query(f"SELECT * FROM {entity_name}s WHERE {entity_name}_id = {entity_id}").fetchall()

        if entity_name == "Song" or entity_name == "Album":
            artist_results = db.execute_query("SELECT name FROM Artists;").fetchall()

            artist_id = db.execute_query("SELECT artist_id FROM " + entity_name + "s WHERE " + entity_name.lower() + "_id = %s", (entity_id,)).fetchone()['artist_id']
            current_artist = db.execute_query("SELECT name FROM Artists WHERE artist_id = %s;", (artist_id,)).fetchone()['name']
            return render_template("edit.html", entity_results=results, artist_fk_data=artist_results, current_artist=current_artist, album_fk_data=[], current_album="", entity_name=entity_name.lower())
        elif entity_name == "Albums_Song":
            song_results = db.execute_query("SELECT song_title FROM Songs;").fetchall()
            album_results = db.execute_query("SELECT album_title FROM Albums;").fetchall()

            song_id = db.execute_query("SELECT song_id FROM Albums_Songs WHERE albums_song_id = %s", (entity_id,)).fetchone()['song_id']
            album_id = db.execute_query("SELECT album_id FROM Albums_Songs WHERE albums_song_id = %s", (entity_id,)).fetchone()['album_id']
            current_song = db.execute_query("SELECT song_title FROM Songs WHERE song_id = %s", (song_id,)).fetchone()['song_title']
            current_album = db.execute_query("SELECT album_title FROM Albums WHERE album_id = %s", (album_id,)).fetchone()['album_title']
            return render_template("edit.html", entity_results=results, artist_fk_data=song_results, current_artist=current_song, album_fk_data=album_results, current_album=current_album, entity_name=entity_name.lower())
        elif entity_name == "Album_Review":
            user_results = db.execute_query("SELECT username FROM Users;").fetchall()
            album_results = db.execute_query("SELECT album_title FROM Albums;").fetchall()

            user_id = db.execute_query("SELECT user_id FROM Album_Reviews WHERE album_review_id = %s", (entity_id,)).fetchone()['user_id']
            album_id = db.execute_query("SELECT album_id FROM Album_Reviews WHERE album_review_id = %s", (entity_id,)).fetchone()['album_id']
            current_user = db.execute_query("SELECT username FROM Users WHERE user_id = %s", (user_id,)).fetchone()['username']
            current_album = db.execute_query("SELECT album_title FROM Albums WHERE album_id = %s", (album_id,)).fetchone()['album_title']
            return render_template("edit.html", entity_results=results, artist_fk_data=user_results, current_artist=current_user, album_fk_data=album_results, current_album=current_album, entity_name=entity_name.lower())
        elif entity_name == "Song_Review":
            user_results = db.execute_query("SELECT username FROM Users;").fetchall()
            song_results = db.execute_query("SELECT song_title FROM Songs;").fetchall()

            user_id = db.execute_query("SELECT user_id FROM Song_Reviews WHERE song_review_id = %s", (entity_id,)).fetchone()['user_id']
            song_id = db.execute_query("SELECT song_id FROM Song_Reviews WHERE song_review_id = %s", (entity_id,)).fetchone()['song_id']
            current_user = db.execute_query("SELECT username FROM Users WHERE user_id = %s", (user_id,)).fetchone()['username']
            current_song = db.execute_query("SELECT song_title FROM Songs WHERE song_id = %s", (song_id,)).fetchone()['song_title']
            return render_template("edit.html", entity_results=results, artist_fk_data=user_results, current_artist=current_user, album_fk_data=song_results, current_album=current_song, entity_name=entity_name.lower())
        else:
            return render_template("edit.html", entity_results=results, artist_fk_data=[], current_artist="", album_fk_data=[], current_album="", entity_name=entity_name.lower())


@app.route('/delete/<entity_name>/<int:entity_id>', methods=['GET', 'POST'])
def delete(entity_name, entity_id):
    """ Handles deletions from any of the tables """

    print(f"Deleting a {entity_name}")
    if request.method == "POST":
        if entity_name == "user":
            db.execute_query(f'DELETE FROM Users WHERE user_id = %s', [entity_id])
            return redirect(url_for(entity_name.lower() + "s"))
        elif entity_name == "albums_song":
            db.execute_query(f'DELETE FROM Albums_Songs WHERE albums_song_id = %s', [entity_id])
            return redirect(url_for(entity_name.lower() + "s"))


    return redirect(url_for(entity_name.lower() + 's'))

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 58766)) 
    app.run(port=port, debug=True) 