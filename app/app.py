import os
import pickle
import tweepy
from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from tweepy import StreamListener, Stream, Cursor
import config

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

import models

class MyStreamListener(StreamListener):
    def on_status(self, status):
        _tweet = status.text
        username = status.user.screen_name
        #_intent = #load model and run predictions
        db_tweet = models.Tweets(
            tweet=_tweet,
            user=username,
            intent=_intent
        )
        db.session.add(db_tweet)
        db.session.commit()
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False # disconnect the stream

def stream_data():
    """Stream tweets from twitter."""
    
    consumerKey = config.CONSUMER_KEY
    consumerSecret = config.CONSUMER_SECRET
    accessToken = config.ACCESS_TOKEN
    accessTokenSecret = config.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    _listener = MyStreamListener()
    my_stream = Stream(auth=api.auth, listener=_listener)
    rules = ['suicide', 'commit suicide', 'suicidal']
    my_stream.filter(track=rules)



@app.route("/app/home/")
def index():
    """Suicide monitor homepage."""
    return render_template("index.html")

@app.route("/app/home/login/", methods=["POST"])
def login():
    """Login route."""
    email = request.form.get("email")
    password = request.form.get("password")
    user = models.Users.query.filter_by(email=email).first()
    if user:
        return redirect("/app/admin_dashboard/")
    else:
        flash("Invalid email/password address.")

    return redirect("/app/home/")
    
    
@app.route("/app/home/search/", methods=["POST"])
@app.route("/app/admin_dashboard/search/", methods=["POST"])
def search_tweets():
    """Search tweets from twitter."""
    from sklearn.feature_extraction.text import CountVectorizer
    import pandas as pd
    import numpy as np
    import re
    import xgboost as xgb
    
    consumerKey = config.CONSUMER_KEY
    consumerSecret = config.CONSUMER_SECRET
    accessToken = config.ACCESS_TOKEN
    accessTokenSecret = config.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    #rules = models.Keywords.query.all()
    #rules = [word.serialize(_id=False)["Keyword"] for word in keywords]
    rule = str(request.form.get("search"))
    rules = ["".join(r for r in rule)]
    print(f"Rules: {rules}")
    Count = 10
    public_tweets = Cursor(api.search, rules, lang="en").items(Count)
    unwanted_words = ['@', 'RT', ':', 'https', 'http']
    symbols = ['@', '#']
    single_chars = re.compile(r'\s+[a-zA-Z]\s+')
    data = []
    for tweet in public_tweets:
        text = tweet.text
        textWords = text.split()
        cleaning_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text).split())
        cleaning_tweet = single_chars.sub('', cleaning_tweet)
        data.append(cleaning_tweet)
    data = pd.DataFrame(data)

    test_data = np.array(data)
    vectorizer = CountVectorizer()
    tokens = vectorizer.fit_transform(data.loc[1:, 0])
    for i, c in enumerate(test_data, 1):
        str_to_vec = vectorizer.transform(c)
        model = xgb.XGBClassifier(nthread=2)
        model.load_model("./saved_models/model.bin")

        pred = model.predict_proba(str_to_vec)[:,1]
        flash(f"Tweet: {str(c[0])}:\n Suicidal_Probability: {np.round(pred[0], 4)}")
     
        return jsonify({'Prediction': str(pred[0]),
                    'Tweet': str(c[0])
    })#render_template("admin.html", tweets=public_tweets)

@app.route("/app/admin_dashboard/")
def admin_home():
    """Admin dashboard home."""
    try:
        keywords = models.Keywords.query.all()
        keywords = [word.serialize() for word in keywords]
        return render_template("admin.html", keywords=keywords)
    except Exception as e:
        return str(e)

@app.route("/app/add-user/")
def add_user():
    name = request.args.get("name")
    email = request.args.get("email")
    role = request.args.get("role")
    password = request.args.get("password")
    try:
        user = models.Users(
            name=name,
            email=email,
            role=role,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for(admin_home))
    except Exception as e:
        return str(e)

@app.route("/app/admin_dashboard/add/", methods=["POST"])
def add_keyword():
    """Add a new keyword to the keyword database."""
    keyterm = request.form.get("add-rule")
    if len(keyterm) >= 4:
        try:
            keyword = models.Keywords(
                keyword=keyterm.lower()
            )
            db.session.add(keyword)
            db.session.commit()

            message = f"Keyword {keyword.id}: {keyword.keyword} added Successfully"
            flash(message)

            keywords = models.Keywords.query.all()
            keywords = [word.serialize() for word in keywords]
            return render_template("admin.html", keywords=keywords)
        except Exception as e:
            return str(e)
    else:
        flash("Invalid argument length. Keywords must be longer than 5 characters")
    return redirect("/app/admin_dashboard/")

@app.route("/app/admin_dashboard/delete/", methods=["POST"])
def delete_keyword():
    """Delete input keyword from the database."""
    key_word = request.form.get("delete-rule")
    try:
        keyword_ = models.Keywords.query.filter_by(keyword=key_word).first()
        db.session.delete(keyword_)
        db.session.commit()
        
        keywords = models.Keywords.query.all()
        keywords = [word.serialize() for word in keywords]
        return render_template("admin.html", keywords=keywords)
    except Exception as e:
        return str(e)




if __name__ == "__main__":
    app.run()
