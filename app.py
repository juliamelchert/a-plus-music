from flask import Flask, render_template, redirect, url_for
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/song-reviews', methods=['GET', 'POST'])
def song_reviews():

    query = "SELECT * FROM Song_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Song Reviews")

@app.route('/album-reviews', methods=['GET', 'POST'])
def album_reviews():

    query = "SELECT * FROM Album_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Album Reviews")

@app.route('/songs', methods=['GET', 'POST'])
def songs():

    query = "SELECT * FROM Songs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Songs")

@app.route('/albums', methods=['GET', 'POST'])
def albums():

    query = "SELECT * FROM Albums;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Albums")

@app.route('/albums-songs', methods=['GET', 'POST'])
def albums_songs():

    query = "SELECT * FROM Albums_Songs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Albums_Songs")

@app.route('/artists', methods=['GET', 'POST'])
def artists():

    query = "SELECT * FROM Artists;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Artists")

@app.route('/users', methods=['GET', 'POST'])
def users():

    query = "SELECT * FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Users")

@app.route('/add/<review_type>-review', methods=['GET', 'POST'])
def add_review(review_type):

    if review_type == "albums_song":
        review_type = "Albums_Song"
    else:
        review_type = review_type.capitalize()

    query = f"SELECT {review_type.lower()}_title FROM {review_type}s;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("add_review.html", media_type=review_type, media_list=results)

@app.route('/add/<entity_name>', methods=['GET', 'POST'])
def add_entity(entity_name):

    if entity_name == "albums_song":
        entity_name = "Albums_Song"
    else:
        entity_name = entity_name.capitalize()

    query = f"SELECT * FROM {entity_name}s;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("add_entity.html", entity_results=results, entity_name=entity_name)

@app.route('/edit/<entity_name>/<entity_id>', methods=['GET', 'POST'])
def edit(entity_name, entity_id):

    if entity_name == "album_reviews":
        entity_name = "Album_Review"
    elif entity_name == "song_reviews":
        entity_name = "Song_Review"
    else:
        entity_name = entity_name.capitalize()

    if entity_name == "Albums_songs":
        query = f"SELECT * FROM Albums_Songs WHERE album_song_id = {entity_id};"
        entity_name = "Albums_Song"
    else:
        query = f"SELECT * FROM {entity_name}s WHERE {entity_name.lower()}_id = {entity_id};"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("edit.html", entity_results=results, entity_name=entity_name)


@app.route('/delete/<entity_name>', methods=['GET', 'POST'])
def delete(entity_name):

    print(f"Deleting a {entity_name.capitalize()}")

    return redirect(url_for(entity_name.lower() + 's'))

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 