from flask import render_template, url_for, redirect, request, session
from reviewhub import app, db
from reviewhub.models import User, Review, Company


@app.route("/")
def home():
    return render_template("reviews.html")


@app.route("/companies")
def companies():
    companies = list(Company.query.all())
    return render_template("companies.html", companies=companies)


# 1. Add a company
@app.route("/add_company", methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        company = Company(company_name=request.form.get('company_name'))
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('companies'))
    return render_template("add_company.html")


# 2.Edit a company
@app.route("/edit_company/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == "POST":
        company.company_name = request.form.get('company_name')
        db.session.commit()
        return redirect(url_for('companies'))
    return render_template('edit_company.html', company=company)


# 3. Delete a company
@app.route("/delete_company/<int:company_id>")
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    return redirect(url_for('companies'))
