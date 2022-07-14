from flask import render_template, url_for, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from reviewhub import app, db
from reviewhub.models import User, Review, Company


# Homepage - View reviews
@app.route("/")
def home():
    reviews = list(Review.query.all())
    return render_template("reviews.html", reviews=reviews)


# Companies page - View companies
@app.route("/view_companies")
def view_companies():
    companies = list(Company.query.all())
    return render_template("view_companies.html", companies=companies)


# 1. Add a company
@app.route("/add_company", methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        company = Company(service_name=request.form.get('service_name'))
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('view_companies'))
    return render_template("add_company.html")


# 2.Edit a company
@app.route("/edit_company/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == "POST":
        company.service_name = request.form.get('service_name')
        db.session.commit()
        return redirect(url_for('view_companies'))
    return render_template('edit_company.html', company=company)


# 3. Delete a company
@app.route("/delete_company/<int:company_id>")
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    return redirect(url_for('view_companies'))


# 1. Add a review
@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    companies = list(Company.query.all())
    if request.method == "POST":
        review = Review(
            company_name=request.form.get('company_name'),
            description=request.form.get('description'),
            created_by=request.form.get('created_by'),
            company_id=request.form.get('company_id')
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_review.html", companies=companies)


# 2. Edit a review
@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    companies = list(Company.query.all())
    if session["user"] == review.created_by:
        if request.method == "POST":
            review.company_name = request.form.get('company_name'),
            review.description = request.form.get('description')
            review.company_id = request.form.get('company_id')
            db.session.commit()
            return redirect(url_for('my_account', username=session["user"]))
    else:
        flash("You can only edit your own reviews")
        return redirect(url_for('my_account', username=session["user"]))
    return render_template(
        "edit_review.html", companies=companies, review=review)


# 3. Delete a review
@app.route("/delete_review/<int:review_id>")
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if session["user"] == review.created_by or session["user"] == "admin@gmail.com":
        db.session.delete(review)
        db.session.commit()
    else:
        flash("You can only delete your own reviews")
    return redirect(url_for('home'))


# Register a user
@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        # first check if they already registered
        existing_user = User.query.filter(
            User.username == request.form.get("username")).all()
        if existing_user:
            print("user already exists")
            flash("Account already exists, please log in")
            return redirect(url_for("register_user"))
        # if not, add them
        user = User(
            username=request.form.get('username').lower(),
            password=generate_password_hash(request.form.get('password')),
        )
        db.session.add(user)
        db.session.commit()
        # Put user into session cookie
        session["user"] = request.form.get('username').lower()
        return redirect(url_for('my_account', username=session['user']))
    return render_template("register_user.html")


# My account
@app.route("/my_account/<username>")
def my_account(username):
    reviews = list(Review.query.all())
    return render_template("my_account.html", username=session["user"], reviews=reviews)


# Log in
@app.route("/login", methods=["GET", "POST"])
def login():
    # Check user exists
    if request.method == "POST":
        existing_user = User.query.filter(
            User.username == request.form.get("username")
        )
        if existing_user:
            print("user found")
            # Check password
            if check_password_hash(
                existing_user[0].password, request.form.get("password")
            ):
                print("password matches")
                session["user"] = request.form.get("username").lower()
                return redirect(url_for('my_account', username=session["user"]))
            else:
                print("password not found")
                return redirect(url_for('login'))
        else:
            flash("User not found, please login")
            return redirect(url_for("login"))
    return render_template('login.html')


# Logout
@app.route("/logout")
def logout():
    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for('home'))
