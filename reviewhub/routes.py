from flask import render_template, request, redirect, url_for
from reviewhub import app, db
from reviewhub.models import User


# Display the homepage
@app.route("/")
def home():
    return render_template("home.html")



# Add a user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            first_name = request.form.get('first_name'),
            last_name = request.form.get('last_name'),
            email = request.form.get('email'),
            password = request.form.get('password'),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('register.html')