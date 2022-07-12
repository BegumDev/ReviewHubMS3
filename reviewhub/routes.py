from flask import render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from reviewhub import app, db, mongo
from reviewhub.models import User, Services


# View services on homepage
@app.route("/")
def home():
    reviews = list(mongo.db.reviews.find())
    return render_template('home.html', reviews=reviews)


# 1. Register a user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # first check if they already registered
        existing_user = User.query.filter(
            User.email == request.form.get("email")).all()
        if existing_user:
            print("user already exists")
            return redirect(url_for("register"))
        # if not, add them
        user = User(
            email=request.form.get('email').lower(),
            password=generate_password_hash(request.form.get('password')),
        )
        db.session.add(user)
        db.session.commit()
        # then put user into session cookie
        session["user"] = request.form.get('email').lower()
        return redirect(url_for("my_account", username=session["user"]))
    return render_template('register.html')


# 2. My account once registered
@app.route("/my_account/<username>", methods=["GET", "POST"])
def my_account(username):
    if "user" in session:
    
        reviews = mongo.db.reviews.find({'created_by': session["user"]})


        return render_template('my_account.html', username=session["user"], reviews=reviews)
    return redirect(url_for("home"))


# 3. Log out of the my account page
@app.route("/logout")
def logout():
    session.pop("user")
    flash("Logout successful")
    return redirect(url_for('home'))


# Log in to my account
@app.route("/login", methods=["GET", "POST"])
def login():
    # check of the user exists
    if request.method == "POST":
        existing_user = User.query.filter(
            User.email == request.form.get("email")).all()
        if existing_user:
            print("existing user found")
            # if they do, check the password
            if check_password_hash(
                existing_user[0].password, request.form.get("password")
            ):
                print("password found")
                session["user"] = request.form.get('email')
                return redirect(url_for("my_account", username=session["user"]))
            else:
                print("password not found")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return(render_template('login.html'))


# 1. Add a review
@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        review = {
            "service_name": request.form.get("service_name"),
            "review": request.form.get("review"),
            "created_by": session["user"]
        }
        mongo.db.reviews.insert_one(review)
        return redirect(url_for("home"))
    return render_template("add_reviews.html")


# Edit a review
@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    if session["user"] == review["created_by"]:
        if request.method == "POST":
            review = {
                "service_name": request.form.get("service_name"),
                "review": request.form.get("review"),
                "created_by": session["user"]
            }
            mongo.db.reviews.replace_one({"_id": ObjectId(review_id)}, review)
            return redirect(url_for('home'))
    else:
        flash("You can only edit your own reviews.")
        return redirect(url_for('home'))
    return render_template("edit_review.html", review=review)


# Delete a review
@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    if session["user"] == review["created_by"]:
        mongo.db.reviews.find_one_and_delete({"_id": ObjectId(review_id)}, review)
        return redirect(url_for('home'))
    else:
        flash("You can only delete your own reviews.")
        return redirect(url_for('home'))

