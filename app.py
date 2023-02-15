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

    return render_template("reviews.html", reviews=results)

@app.route('/album-reviews')
def album_reviews():

    query = "SELECT * FROM Album_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("reviews.html", reviews=results)

@app.route('/post-review')
def post_review():

    return render_template("post_review.html")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 