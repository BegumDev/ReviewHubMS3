"""
Import modules
"""
from flask import render_template, url_for, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from reviewhub import app, db
from reviewhub.models import User, Review, Company


# Homepage - View reviews
@app.route("/")
def home():
    """
    Routes the user back to the homepage and displays all reviews
    """
    reviews = list(Review.query.all())
    return render_template("reviews.html", reviews=reviews)


# Companies page - View companies
@app.route("/view_companies")
def view_companies():
    """
    Enables admin to view and manage companies and reviews
    """
    companies = list(Company.query.all())
    reviews = list(Review.query.all())
    return render_template(
        "view_companies.html", companies=companies, reviews=reviews)


# 1. Add a company
@app.route("/add_company", methods=["GET", "POST"])
def add_company():
    """
    GET: the company form
    POST: the new addition to the view_companies page.
    """
    if request.method == "POST":
        company = Company(service_name=request.form.get('service_name'))
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('view_companies'))
    return render_template("add_company.html")


# 2.Edit a company
@app.route("/edit_company/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    """
    GET: the edit-company form
    POST: the changes to the view_companies page
    """
    company = Company.query.get_or_404(company_id)
    if request.method == "POST":
        company.service_name = request.form.get('service_name')
        db.session.commit()
        return redirect(url_for('view_companies'))
    return render_template('edit_company.html', company=company)


# 3. Delete a company
@app.route("/delete_company/<int:company_id>")
def delete_company(company_id):
    """
    Allows admin to delete a company. Note this will delete associated reviews.
    """
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    return redirect(url_for('view_companies'))


# 1. Add a review
@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    """
    GET: the add_review form
    POST: the new addition to the reviews page.
    """
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


# Edit a review
@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    """
    GET: the edit-review form
    POST: the changes to the reviews page
    """
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
    """
    Allows users to delete their own review.
    """
    review = Review.query.get_or_404(review_id)
    if session["user"] == review.created_by or session["user"] == "admin@gmail.com":  # noqa ES501
        db.session.delete(review)
        db.session.commit()
        if session["user"] == "admin@gmail.com":
            return redirect(url_for('view_companies'))
        else:
            return redirect(url_for('my_account', username=session["user"]))
    else:
        flash("You can only delete your own reviews")
        return redirect(url_for('home'))


# Register a user
@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    """
    Registers a user;

    """
    if request.method == "POST":
        # first check if they already registered
        existing_user = User.query.filter(
            User.username == request.form.get("username")).all()
        if existing_user:
            flash("Account already exists, please log in")
            return redirect(url_for("login"))
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


def is_user_logged_in():
    """
    Checks if any user is logged in
    """
    return 'user' in session

# My account


@app.route("/my_account/<username>")
def my_account(username):
    """
    Routes the user to their own account and own reviews on successful log in.
    """
    if not is_user_logged_in():
        return redirect(url_for('login'))

    is_admin = session['user'] == "admin@gmail.com"
    reviews = list(Review.query.filter_by(created_by=session['user']))
    return render_template(
        "my_account.html", username=session["user"], name=username,
        reviews=reviews, is_admin_user=is_admin)


# Log in
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Enables users to log back into their account
    """
    # Check user exists
    if request.method == "POST":
        existing_user = User.query.filter(
            User.username == request.form.get("username")
        ).all()
        if existing_user:
            # Check password
            if check_password_hash(
                existing_user[0].password, request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                if session["user"] == "admin@gmail.com":
                    return redirect(url_for('view_companies'))
                else:
                    return redirect(url_for('my_account',
                    username=session["user"]))  # noqa E128
            else:
                flash('Sorry incorrect username/password')
                return redirect(url_for('login'))
        else:
            flash("User not found, please register")
            return redirect(url_for('register_user'))
    return render_template('login.html')


# Logout
@app.route("/logout")
def logout():
    """
    Logs a user out and routes them back to the login page.
    """
    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for('login'))


# Send email
@app.route('/contact_us')
def contact_us():
    """
    Renders the email contact form page.
    """
    return render_template("contact.html")


# Error handling - page not found
@app.errorhandler(404)
def page_not_found(e):
    """
    Returns a 404 page with a button to guide back to the homepage.
    """
    print(e)
    return render_template('404.html', title='404 - Page Not Found'), 404


# Search funcitonality
@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Allows users to search reviews using coompany name or description keywords
    """
    if request.method == "POST":
        query = request.form.get('query')

        company_name = "%{}%".format(query)
        company_results = Review.query.filter(
            Review.company_name.like(company_name)).all()

        searched = "%{}%".format(query)
        description_results = Review.query.filter(
            Review.description.like(searched)).all()

    return render_template(
        "search_results.html", description_results=description_results,
        query=query, company_results=company_results)
