from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from reviewhub import app, db
from reviewhub.models import User, Reviews


# Display the homepage
@app.route("/")
def home():
    return render_template("home.html")


# 1. Register a user
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
            first_name = request.form.get('first_name').lower(),
            last_name = request.form.get('last_name').lower(),
            email = request.form.get('email').lower(),
            password = generate_password_hash(request.form.get('password')),
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
        return render_template('myaccount.html', username=session["user"])
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
        existing_user = User.query.filter(User.email == request.form.get("email")).all()
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


# Add a review
@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        review = Reviews(
            company=request.form.get('company_name'),
            experience=request.form.get('experience'),
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("addreview.html")


# See my reviews
@app.route("/my_reviews")
def my_reviews():
    reviews = Reviews.query.all()
    return render_template("addreview.html", reviews=reviews)


# Edit review
@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = Reviews.query.get_or_404(review_id)
    if request.method == "POST":
        review.company = request.form.get("company_name")
        review.experience = request.form.get("experience")
        db.session.commit()
        return redirect(url_for("my_reviews"))
    return render_template("edit_review.html", review=review)