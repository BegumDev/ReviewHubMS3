from flask import render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from reviewhub import app, db, mongo
from reviewhub.models import User, Services


# View services on homepage
@app.route("/")
def home():
    service_list = Services.query.all()
    return render_template("home.html", service_list=service_list)


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
        return render_template('my_account.html', username=session["user"])
    return redirect(url_for("home"))


# 3. Log out of the my account page
@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for('login'))


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
                if session["user"] == "admin@gmail.com":
                    return redirect(url_for('admin_page'))
                return redirect(url_for("my_account", username=session["user"]))
            else:
                print("password not found")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return(render_template('login.html'))


# Admin page
@app.route("/admin_page")
def admin_page():
    return render_template('admin_page.html')


# 1. Add a service
@app.route("/add_service", methods=["GET", "POST"])
def add_service():
    if request.method == "POST":
        service = Services(service_name=request.form.get("service_name"))
        db.session.add(service)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_service.html")


# 2. Edit a service
@app.route("/edit_service/<int:service_id>", methods=["GET", "POST"])
def edit_service(service_id):
    change = Services.query.get_or_404(service_id)
    if request.method == "POST":
        change.service_name = request.form.get('service_name')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_services.html', change=change)


# 3. Delete a service
@app.route("/delete_service/<int:service_id>")
def delete_service(service_id):
    service = Services.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('home'))
    return render_template('home.html')


# View reviews
@app.route("/get_reviews")
def get_reviews():
    reviews = mongo.db.reviews.find()
    return render_template("get_reviews.html", reviews=reviews)


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        review = {
            "service_name": request.form.get("service_name"),
            "review": request.form.get("review"),
        }
        mongo.db.tasks.insert_one(review)
        return redirect(url_for("home"))
    return render_template("get_reviews.html")