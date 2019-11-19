from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import web_scrape
import pandas as pd

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/social_app"
mongo = PyMongo(app)

mongo.db.mars.update({}, {}, upsert=True)

@app.route("/")
def index():
    try:
        mars_info = mongo.db.mars.find_one()
        title = mars_info['news_title']
        paragraph = mars_info['news_paragraph']
        df = pd.read_csv("data.csv")
        df = df.set_index('Attributes')
        tweet = mars_info['latest_tweet']
        image_dict = mars_info['images']
        keys = []
        for key in image_dict:
            keys.append(key)

        return render_template("index.html", title=title, paragraph=paragraph, tables=df.to_html(), titles=['mars'], tweet=tweet, images=image_dict, hem_names=keys)
    except Exception:
        return render_template("index.html")

@app.route("/scrape")
def mars():
    mongo.db.mars.update({}, {}, upsert=True)
    mars = mongo.db.mars
    mars_info = web_scrape.scrape()
    mars.update({}, mars_info, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)