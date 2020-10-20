import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

import models #Keywords, Users, Tweets

@app.route("/admin_dashboard")
def home():
    return render_template("admin.html")

@app.route("/admin_dashboard", methods=["POST"])
def add_keyword():
    """Add a new keyword to the keyword database."""
    if request.method == "POST":
        keyterm = request.form.get("add-rule")
        try:
            keyword = models.Keywords(
                keyword=keyterm
            )
            db.session.add(keyword)
            db.session.commit()

            message = f"Keyword {keyword.id}: {keyword.keyword} added Successfully"
            
        except Exception as e:
            return str(e)
    return render_template("admin.html")

@app.route("/admin_dashboard")
def get_keywords():
    """Return all available keywords."""
    try:
        keywords = models.Keywords.query.all()
        keywords = jsonify([word.serialize() for word in keywords])
    except Exception as e:
        return str(e)




if __name__ == "__main__":
    app.run()
