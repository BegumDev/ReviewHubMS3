from reviewhub import db


class Company(db.Model):
    # schema for the company name
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(40), unique=True, nullable=False)
    reviews = db.relationship(
        "Review", backref="company", cascade="all, delete", lazy=True)

    def __repr__(self):
        # to represent itself as a string
        return self.company_name


class Review(db.Model):
    # schema for the review
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(
        "company.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # to represent itself as a string
        return f"#{self.id} - Review: {self.description}"


class User(db.Model):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        # to represent itself as a string
        return self.username
