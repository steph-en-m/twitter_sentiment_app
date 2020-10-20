from app import db

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.Integer)
    role = db.Column(db.String())

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __repr__(self):
        return f"<id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role
        }

class Keywords(db.Model):
    __tablename__="keywords"
    id  = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String())

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return f"<id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "Keyword": self.keyword
            }

class Tweets(db.Model):
    __tablename__="tweets"
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String())
    intent = db.Column(db.String())
    user = db.Column(db.String())

    def __init__(self, tweet, user):
        self.tweet = tweet
        self.user = user

    def __repr__(self):
        return f"<id {self.id}>"

    def serialize(self):
        return {
            "Tweet": self.tweet,
            "User": self.user
        }
