from reviewhub import db

class Categories(db.Model):
    # schema for the Categories model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.id = id
        self.category_name = category_name


