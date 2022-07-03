from reviewhub import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)

    def __repr__(self):
        self.id = id
        self.email = email
        self.password = password


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.Text)

    def __repr__(self):
        self.id = id
        self.service = service