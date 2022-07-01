from reviewhub import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.Text)
    password = db.Column(db.Text)

    def __repr__(self):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.Text)
    experience = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        self.id = id
        self.company = company
        self.experience = experience