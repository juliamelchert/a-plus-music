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

@app.route('/<review_type>-review/add', methods=['GET', 'POST'])
def add_review(review_type):
    """ Handles creations of Song_Reviews and Album_Reviews """

    if request.method == "GET":
        results = get_add_review_info(review_type)

    elif request.method == "POST":
        return redirect(url_for(review_type + "_reviews"))

    return render_template("add_review.html", media_type=review_type, media_list=results[0], users=results[1])

@app.route('/<entity_name>/add', methods=['GET', 'POST'])
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
        
        # Insert into Songs table
        if entity_name == "song":
            add_song(get_artist_id_from_name(request.form['fk_data_2']), request.form['song_title'], request.form['song_genre'])
            return redirect(url_for("songs"))

        # Insert into Albums table
        elif entity_name == "album":
            add_album(get_artist_id_from_name(request.form['fk_data_2']), request.form['album_title'], request.form['album_genre'])
            return redirect(url_for("albums"))

        # Insert into Artists table
        elif entity_name == "artist":
            add_artist(request.form['name'])
            return redirect(url_for("artists"))

        # Insert into Users table
        elif entity_name == "user":
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
    
def capitalize_entity_name(original_entity_name):
    """ Fixes the capitalization of an entity name such that it can be used as the table name in a query """
    if original_entity_name == "albums_song":
        return "Albums_Song"
    elif original_entity_name == "song_review":
        return "Song_Review"
    elif original_entity_name == "album_review":
        return "Album_Review"
    else:
        return original_entity_name.capitalize()

@app.route('/<entity_name>/edit/<int:entity_id>', methods=('GET', 'POST'))
def edit(entity_name, entity_id):
    """ Handles updates to any entity in any of the tables """

    # Handle GET requests from loading the page
    if request.method == "GET":
        entity_name = capitalize_entity_name(entity_name)
        results = get_star_entity_where_id(entity_name, entity_id)

        if entity_name == "Song" or entity_name == "Album":
            current_artist = get_artist_name_from_id(get_current_artist_id_from_table(entity_name, entity_id))
            return render_template("edit.html", entity_results=results, entity_name=entity_name.lower(), artist_fk_data=get_artist_names(), current_artist=current_artist, album_fk_data=[], current_album="")
        
        elif entity_name == "Albums_Song":
            current_song = get_song_title_from_id(get_albums_song_song_id(entity_id))
            current_album = get_album_title_from_id(get_albums_song_album_id(entity_id))
            return render_template("edit.html", entity_results=results, entity_name=entity_name.lower(), artist_fk_data=get_song_titles(), current_artist=current_song, album_fk_data=get_album_titles(), current_album=current_album)
        
        elif entity_name == "Album_Review":
            current_user = get_username_from_user_id(get_user_id_from_review_id(entity_name, entity_id))
            current_album = get_album_title_from_id(get_album_id_from_album_review_id(entity_id))
            return render_template("edit.html", entity_results=results, entity_name=entity_name.lower(), artist_fk_data=get_usernames(), current_artist=current_user, album_fk_data=get_album_titles(), current_album=current_album)
        
        elif entity_name == "Song_Review":
            current_user = get_username_from_user_id(get_user_id_from_review_id(entity_name, entity_id))
            current_song = get_song_title_from_id(get_song_id_from_song_review_id(entity_id))
            return render_template("edit.html", entity_results=results, entity_name=entity_name.lower(), artist_fk_data=get_usernames(), current_artist=current_user, album_fk_data=get_song_titles(), current_album=current_song)
        
        else:
            return render_template("edit.html", entity_results=results, entity_name=entity_name.lower(), artist_fk_data=[], current_artist="", album_fk_data=[], current_album="")

    # This if-statement section is adapted from the official Flask tutorial (https://flask.palletsprojects.com/en/2.2.x/tutorial/)
    # Handle POST requests from editing an entity
    elif request.method == "POST":
        if entity_name == "song":
            edit_song(get_artist_id_from_name(request.form['artist_fk_data']), request.form['song_title'], request.form['song_genre'], entity_id)

        elif entity_name == "album":
            edit_album(get_artist_id_from_name(request.form['artist_fk_data']), request.form['album_title'], request.form['album_genre'], entity_id)

        elif entity_name == "artist":
            edit_artist(request.form['name'], entity_id)
        
        elif entity_name == "user":
            edit_user(request.form['username'], request.form['email'], entity_id)

        elif entity_name == "albums_song":
            album_id = get_album_id_from_title(request.form['album_fk_data'])
            song_id = get_song_id_from_title(request.form['song_fk_data'])
            edit_albums_song(album_id, song_id, entity_id)

        return redirect(url_for(entity_name + "s"))

@app.route('/<entity_name>/delete/<int:entity_id>', methods=['GET', 'POST'])
def delete(entity_name, entity_id):
    """ Handles deletions from any of the tables """

    if request.method == "POST":
        if entity_name == "song":
            delete_song(entity_id)
        elif entity_name == "album":
            delete_album(entity_id)
        elif entity_name == "artist":
            delete_artist(entity_id)
        elif entity_name == "user":
            delete_user(entity_id)
        elif entity_name == "albums_song":
            delete_albums_song(entity_id)
        elif entity_name == "song_review":
            delete_song_review(entity_id)
        elif entity_name == "album_review":
            delete_album_review(entity_id)

    return redirect(url_for(entity_name + 's'))

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 58766)) 
    app.run(port=port, debug=True) 