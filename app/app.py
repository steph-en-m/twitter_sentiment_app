import os
import re
import pickle
import tweepy
from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from tweepy import StreamListener, Stream, Cursor
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import xgboost as xgb
#from . import app_config

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

import models

# Tweepy Configurations
CONSUMER_KEY = "25O70MpmGuKOVn2z4q6Pnqg0g"
CONSUMER_SECRET = "RhsCbkW1IvqWywqXGeNl7zOzcfCFGBEnpx07Csk9lHLe0OXtdw"
ACCESS_TOKEN = "940556535222231040-YwDy453At4zZkZBKD1no1wLOSFbnXW4"
ACCESS_TOKEN_SECRET = "Z7vuvj4jauPJuy51MdHw8lc3HtGLh2df5bCsubjCQDsxB"

def fetch_tweets():
    """Fetch tweets from twitter."""
    consumerKey = CONSUMER_KEY
    consumerSecret = CONSUMER_SECRET
    accessToken = ACCESS_TOKEN
    accessTokenSecret = ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    rules = models.Keywords.query.all()
    rules = [word.serialize(_id=False)["Keyword"] for word in rules]
    
    n_tweets = 45
    public_tweets = Cursor(api.search, rules[:2], lang="en").items(n_tweets)
    unwanted_words = ['@', 'RT', ':', 'https', 'http']
    symbols = ['@', '#']
    single_chars = re.compile(r'\s+[a-zA-Z]\s+')
    data = []
    users = []
    for tweet in public_tweets:
        text = tweet.text
        usr = tweet.user.screen_name
        users.append(usr)
        textWords = text.split()
        cleaning_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text).split())
        cleaning_tweet = single_chars.sub('', cleaning_tweet)
        data.append(cleaning_tweet)
    data = pd.DataFrame(data)
    #print(f"Users: {users}")

    test_data = np.array(data)
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1,3))
    vectorizer = pickle.load(open('./saved_models/vectorizer.pkl', 'rb'))
    results = []
    ct = 0
    for i, c in enumerate(test_data, 1):
        str_to_vec = vectorizer.transform(c)
        model = xgb.XGBClassifier(nthread=2)
        model.load_model("./saved_models/model.bin")
        usr_ = users[ct]
        ct += 1
        pred = model.predict_proba(str_to_vec)[:,1]
        intent_ = ""
        if pred[0] <= 0.4:
            intent_ = "Not Suicidal"
        elif pred[0] > 0.4 and pred[0] <= 0.6:
            intent_ = "Neutral"
        else:
            intent_ = "Suicidal"
        result = {
            'User': '@'+usr_,
            'Tweet': str(c[0]),
            'Prediction': intent_
                 }
        results.append(result)
        # add tweet and meta to the db
        tweet_ = models.Tweets(
                               tweet=str(c[0]),
                               user='@'+usr_,
                               intent=intent_
                               )
        db.session.add(tweet_)
        db.session.commit()

    suicidal_tweet_count = 0
    nonsuicidal_tweet_count = 0
    neutral_tweet_count = 0
    # sequences
    suicidal_seq = [0]
    non_suicidal_seq = [0]
    neutral_seq = [0]
    for t in results:
        if t["Prediction"] == "Suicidal":
            suicidal_tweet_count += 1
            suicidal_seq.append(suicidal_tweet_count)
        elif t["Prediction"] == "Not Suicidal":
            nonsuicidal_tweet_count += 1
            non_suicidal_seq.append(nonsuicidal_tweet_count)
        else:
            neutral_tweet_count += 1
            neutral_seq.append(neutral_tweet_count)
    counts = []
    counts.append(suicidal_tweet_count)
    counts.append(nonsuicidal_tweet_count)
    counts.append(neutral_tweet_count)
    counts_dict = {"counts": counts}
    # tweet sequence
    counts_seq = {"suidical": suicidal_seq[:7],
                  "non_suicidal": non_suicidal_seq[:7],
                  "neutral": neutral_seq[:7]
                  }
    print(f'Counts_seq: {counts_seq}')

    return results, counts_dict, counts_seq

@app.route("/")
@app.route("/app/home/")
def index():
    """Suicide monitor homepage."""
    results, counts_dict, counts_seq = fetch_tweets()
    
    #counts_dict = {"counts": counts}
    return render_template("index.html",
                            tweets=results,
                            counts=counts_dict,
                            counts_seq=counts_seq
                           )

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
    consumerKey = CONSUMER_KEY
    consumerSecret = CONSUMER_SECRET
    accessToken = ACCESS_TOKEN
    accessTokenSecret = ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    rule = str(request.form.get("search"))
    rules = ["".join(r for r in rule)]
    #print(f"Rules: {rules}")
    Count = 45
    public_tweets = Cursor(api.search, rules, lang="en").items(Count)
    unwanted_words = ['@', 'RT', ':', 'https', 'http']
    symbols = ['@', '#']
    single_chars = re.compile(r'\s+[a-zA-Z]\s+')
    data = []
    users = []
    for tweet in public_tweets:
        text = tweet.text
        usr = tweet.user.screen_name
        users.append(usr)
        textWords = text.split()
        cleaning_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text).split())
        cleaning_tweet = single_chars.sub('', cleaning_tweet)
        data.append(cleaning_tweet)
    data = pd.DataFrame(data)

    test_data = np.array(data)
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1,3))
    vectorizer = pickle.load(open('./saved_models/vectorizer.pkl', 'rb'))
    results = []
    ct = 0
    for i, c in enumerate(test_data, 1):
        str_to_vec = vectorizer.transform(c)
        model = xgb.XGBClassifier(nthread=2)
        model.load_model("./saved_models/model.bin")
        usr_ = users[ct]
        ct += 1
        pred = model.predict_proba(str_to_vec)[:,1]
        intent_ = ""
        if pred[0] <= 0.4:
            intent_ = "Not Suicidal"
        elif pred[0] > 0.4 and pred[0] <= 0.7:
            intent_ = "Neutral"
        else:
            intent_ = "Suicidal"
        result = {
            'User': '@'+usr_,
            'Tweet': str(c[0]),
            'Prediction': intent_
                 }
        results.append(result)
    suicidal_tweet_count = 0
    nonsuicidal_tweet_count = 0
    neutral_tweet_count = 0
    for t in results:
        if t["Prediction"] == "Suicidal":
            suicidal_tweet_count += 1
        elif t["Prediction"] == "Not Suicidal":
            nonsuicidal_tweet_count += 1
        else:
            neutral_tweet_count += 1
    counts = []
    counts.append(suicidal_tweet_count)
    counts.append(nonsuicidal_tweet_count)
    counts.append(neutral_tweet_count)
    counts_dict = {"counts": counts}
    return render_template("index.html",
                           tweets=results,
                           counts=counts_dict,
                           )

@app.route("/app/admin_dashboard/")
def admin_home():
    """Admin dashboard home."""
    try:
        results, counts_dict, counts_seq = fetch_tweets()

        keywords = models.Keywords.query.all()
        keywords = [word.serialize() for word in keywords]
        return render_template("admin.html",
                                keywords=keywords,
                                tweets=results,
                                counts=counts_dict,
                                counts_seq=counts_seq
                                )
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
            return redirect('/app/admin_dashboard/')
        except Exception as e:
            return str(e)
    else:
        flash("Invalid argument length. Keywords must be longer than 5 characters")
    return redirect("/app/admin_dashboard/")

@app.route("/app/admin_dashboard/delete/", methods=["GET", "POST"])
def delete_keyword():
    """Delete input keyword from the database."""
    key_word = request.form.get("delete-rule")
    try:
        keyword_ = models.Keywords.query.filter_by(keyword=key_word).first()
        db.session.delete(keyword_)
        db.session.commit()
        
        keywords = models.Keywords.query.all()
        keywords = [word.serialize() for word in keywords]
        return redirect("/app/admin_dashboard/")
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run()
