# A+ Music - Music Review Database
*Authors: Julia Melchert and Jeffrey Wang | Date Last Updated: 3/30/2023*

View this website on the internet [here](https://juliamelchert.pythonanywhere.com/)!

This Flask application compiles music-lovers' thoughts on songs and albums to make the search for your next favorite jam easy. The primary user for this website is the administrator of the A+ Music database, so it does not involve many customer-related features like logging in or account creation. However, it does allows users to view, create, update, and delete information relating to the service. Users may view information on any of the seven tables included in the database, as well as manipulate the information in each of those tables through the intuitive UI.

This project utilizes **Python/Flask** for the front-end UI and **MySQL** for the back-end data definition, manipulation, and storage.

The following sources were utilized throughout the project:
* [Oregon State University's CS 340 Flask Starter Guide](https://github.com/osu-cs340-ecampus/flask-starter-app): The db_connector.py file from this project is largely based off of the db_connector.py file from this starter guide.
* [Flask Documentation on Handling Application Errors](https://flask.palletsprojects.com/en/2.2.x/errorhandling/): The error handling functions in app.py as well as the templates in the "errors" directory are largely based off of this Flask documentation page's examples.
* [W3Schools CSS Tables](https://www.w3schools.com/css/css_table.asp): The CSS for the table is largely based on and/or copied from the example code from this article, especially that from [the first try it yourself link](https://www.w3schools.com/css/tryit.asp?filename=trycss_table_fancy). This includes the "hover" and "nth-child(even)" attributes.

This was the final project for CS 340 (Introduction to Databases) at Oregon State University in March 2023.
