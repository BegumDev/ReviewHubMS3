from flask import render_template, request, redirect, url_for, session
from reviewhub import app, db
from reviewhub.models import User


# Display the homepage
@app.route("/")
def home():
    return render_template("home.html")


# 1. Add a user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # first check if they already registered
        existing_user = User.query.filter(User.email == request.form.get("email")).all()
        if existing_user:
            print("user already exists")
            return redirect(url_for("register"))
        # if not, add them
        user = User(
            first_name = request.form.get('first_name'),
            last_name = request.form.get('last_name'),
            email = request.form.get('email'),
            password = request.form.get('password'),
        )
        db.session.add(user)
        db.session.commit()
        # then put user into session cookie
        session["user"] = request.form.get('email').lower()
        return redirect(url_for("my_account", username=session["user"]))
    return render_template('register.html')


# 2. My account once registered
@app.route("/my_account")
def my_account():
    return render_template('myaccount.html')