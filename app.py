from flask import Flask, render_template
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/song-reviews')
def song_reviews():

    query = "SELECT * FROM Song_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("reviews.j2", reviews=results)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 