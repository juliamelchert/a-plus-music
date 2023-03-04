from flask import Flask, render_template, redirect, url_for, request, flash
import database.db_connector as db
from queries import *
import os

# Configuration
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Routes
@app.route('/')
def root():
    return render_template("index.html")

@app.route('/album-reviews', methods=['GET', 'POST'])
def album_reviews():
    """ Displays the Album_Reviews table """

    return render_template("entities/album_reviews.html", album_reviews=get_all_album_reviews())

@app.route('/song-reviews', methods=['GET', 'POST'])
def song_reviews():
    """ Displays the Song_Reviews table """

    return render_template("entities/song_reviews.html", song_reviews=get_all_song_reviews())

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    """ Displays the Albums table """

    return render_template("entities/albums.html", albums=get_all_albums())

@app.route('/albums-songs', methods=['GET', 'POST'])
def albums_songs():
    """ Displays the Albums_Songs table """

    return render_template("entities/albums_songs.html", albums_songs=get_all_albums_songs())

@app.route('/artists', methods=['GET', 'POST'])
def artists():
    """ Displays the Artists table """
    
    return render_template("entities/artists.html", artists=get_all_artists())

@app.route('/songs', methods=['GET', 'POST'])
def songs():
    """ Displays the Songs table """

    return render_template("entities/songs.html", songs=get_all_songs())

@app.route('/users', methods=['GET', 'POST'])
def users():
    """ Displays the Users table """

    return render_template("entities/users.html", users=get_all_users())

@app.route('/add/<review_type>-review', methods=['GET', 'POST'])
def add_review(review_type):
    """ Handles creations of Song_Reviews and Album_Reviews """

    if request.method == "GET":
        results = get_add_review_info(review_type)

    elif request.method == "POST":
        return redirect(url_for(review_type + "_reviews"))

    return render_template("add_review.html", media_type=review_type, media_list=results[0], users=results[1])

@app.route('/add/<entity_name>', methods=['GET', 'POST'])
def add_entity(entity_name):
    """ Handles creations of Songs, Albums, Artists, Users, and Albums_Songs """

    # Handle GET requests from loading the page
    if request.method == "GET":
        if entity_name == "albums_song":
            results = get_star_albums_songs()
        else:
            results = get_star_entity(entity_name)

        # Dynamically generates drop-down menus for different entities
        if entity_name == "song" or entity_name == "album":
            return render_template("add_entity.html", entity_results=results, entity_name=entity_name, fk_data_1=[], fk_data_2=get_artist_names())
        elif entity_name == "albums_song":
            return render_template("add_entity.html", entity_results=results, entity_name=entity_name, fk_data_1=get_album_titles(), fk_data_2=get_song_titles())
        else:
            return render_template("add_entity.html", entity_results=results, entity_name=entity_name, fk_data_1=[], fk_data_2=[])

    # This if-statement section is adapted from the official Flask tutorial (https://flask.palletsprojects.com/en/2.2.x/tutorial/)
    # Handle POST requests from adding an entity
    elif request.method == "POST":
        # Insert into Users table
        if entity_name == "user":
            add_user(request.form['username'], request.form['email'])
            return redirect(url_for("users"))
        
        # Insert into Albums_Songs table
        elif entity_name == "albums_song":
            album_id = get_album_id_from_title(request.form['fk_data_1'])
            song_id = get_song_id_from_title(request.form['fk_data_2'])

            # If the entry already exists, an error is flashed since Albums_Songs additions must be unique
            if check_albums_song_exists(album_id, song_id) == 1:
                flash("This Albums_Songs entry already exists.")
                return redirect(url_for("add_entity", entity_name=entity_name))
            # If the Albums_Songs entry doesn't already exist, it's added
            else:
                add_albums_song(album_id, song_id)
                return redirect(url_for("albums_songs"))
    
@app.route('/edit/<entity_name>/<int:entity_id>', methods=('GET', 'POST'))
def edit(entity_name, entity_id):
    """ Handles updates to any entity in any of the tables """

    # This if-statement section is adapted from the official Flask tutorial (https://flask.palletsprojects.com/en/2.2.x/tutorial/)
    if request.method == "POST":
        if entity_name == "user":
            db.execute_query(f'UPDATE Users SET username = %s, email = %s WHERE user_id = %s', (request.form['username'], request.form['email'], entity_id))

        elif entity_name == "albums_song":
            album_id = db.execute_query('SELECT album_id FROM Albums WHERE album_title = (%s)', (request.form['album_fk_data'],)).fetchone()['album_id']
            song_id = db.execute_query('SELECT song_id FROM Songs WHERE song_title = (%s)', (request.form['song_fk_data'],)).fetchone()['song_id']
            db.execute_query(f'UPDATE Albums_Songs SET album_id = %s, song_id = %s WHERE albums_song_id = %s', (album_id, song_id, entity_id))        

        return redirect(url_for(entity_name + "s"))

    # Handle GET requests from loading the page
    elif request.method == "GET":
        # TODO: Refactor below since it is reused in add_entity path
        if entity_name == "albums_song":
            entity_name = "Albums_Song"
        elif entity_name == "song_review":
            entity_name = "Song_Review"
        elif entity_name == "album_review":
            entity_name = "Album_Review"
        else:
            entity_name = entity_name.capitalize()

        results = get_star_entity_where_id(entity_name, entity_id)

        if entity_name == "Song" or entity_name == "Album":
            artist_results = get_artist_names()

            artist_id = db.execute_query("SELECT artist_id FROM " + entity_name + "s WHERE " + entity_name.lower() + "_id = %s", (entity_id,)).fetchone()['artist_id']
            current_artist = db.execute_query("SELECT name FROM Artists WHERE artist_id = %s;", (artist_id,)).fetchone()['name']
            return render_template("edit.html", entity_results=results, artist_fk_data=artist_results, current_artist=current_artist, album_fk_data=[], current_album="", entity_name=entity_name.lower())
        elif entity_name == "Albums_Song":
            song_results = get_song_titles()
            album_results = get_album_titles()

            song_id = db.execute_query("SELECT song_id FROM Albums_Songs WHERE albums_song_id = %s", (entity_id,)).fetchone()['song_id']
            album_id = db.execute_query("SELECT album_id FROM Albums_Songs WHERE albums_song_id = %s", (entity_id,)).fetchone()['album_id']
            current_song = db.execute_query("SELECT song_title FROM Songs WHERE song_id = %s", (song_id,)).fetchone()['song_title']
            current_album = db.execute_query("SELECT album_title FROM Albums WHERE album_id = %s", (album_id,)).fetchone()['album_title']
            return render_template("edit.html", entity_results=results, artist_fk_data=song_results, current_artist=current_song, album_fk_data=album_results, current_album=current_album, entity_name=entity_name.lower())
        elif entity_name == "Album_Review":
            user_results = get_usernames()
            album_results = get_album_titles()

            user_id = db.execute_query("SELECT user_id FROM Album_Reviews WHERE album_review_id = %s", (entity_id,)).fetchone()['user_id']
            album_id = db.execute_query("SELECT album_id FROM Album_Reviews WHERE album_review_id = %s", (entity_id,)).fetchone()['album_id']
            current_user = db.execute_query("SELECT username FROM Users WHERE user_id = %s", (user_id,)).fetchone()['username']
            current_album = db.execute_query("SELECT album_title FROM Albums WHERE album_id = %s", (album_id,)).fetchone()['album_title']
            return render_template("edit.html", entity_results=results, artist_fk_data=user_results, current_artist=current_user, album_fk_data=album_results, current_album=current_album, entity_name=entity_name.lower())
        elif entity_name == "Song_Review":
            user_results = get_usernames()
            song_results = get_song_titles()

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

    if request.method == "POST":
        if entity_name == "user":
            delete_user(entity_id)
        elif entity_name == "albums_song":
            delete_albums_song(entity_id)

    return redirect(url_for(entity_name + 's'))

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 58766)) 
    app.run(port=port, debug=True) 