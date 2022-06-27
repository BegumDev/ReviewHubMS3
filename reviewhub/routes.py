from flask import render_template
from reviewhub import app, db

# Display the homepage
@app.route("/")
def home():
    return render_template("home.html")