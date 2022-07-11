import os
from reviewhub import app
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG")
    )