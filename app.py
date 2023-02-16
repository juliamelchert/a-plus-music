from flask import Flask, render_template
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():

    return render_template("index.html")

@app.route('/song-reviews')
def song_reviews():

    query = "SELECT * FROM Song_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Song Reviews")

@app.route('/album-reviews')
def album_reviews():

    query = "SELECT * FROM Album_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Album Reviews")

@app.route('/songs')
def songs():

    query = "SELECT * FROM Songs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Songs")

@app.route('/albums')
def albums():

    query = "SELECT * FROM Albums;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Albums")

@app.route('/albums-songs')
def albums_songs():

    query = "SELECT * FROM Albums_Songs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Albums_Songs")

@app.route('/artists')
def artists():

    query = "SELECT * FROM Artists;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("entity.html", entity_results=results, entity_name="Artists")

@app.route('/users')
def users():

    query = "SELECT * FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(f"Results: {results}")

    return render_template("entity.html", entity_results=results, entity_name="Users")

@app.route('/add-<review_type>-review', methods=['GET', 'POST'])
def add_review(review_type):

    review_type = review_type.capitalize()

    query = f"SELECT {review_type.lower()}_title FROM {review_type}s;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("add_review.html", media_type=review_type, media_list=results)

@app.route('/add-<entity_name>', methods=['GET', 'POST'])
def add_entity(entity_name):

    entity_name = entity_name.capitalize()

    query = f"SELECT * FROM {entity_name}s;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("add_entity.html", entity_results=results, entity_name=entity_name)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 