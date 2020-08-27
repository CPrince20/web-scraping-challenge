from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/scrape")
def scrape():
    mars_dictionary = mongo.db.mars_dictionary
    mars_data = scrape_mars.scrape()
    mars_dictionary.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

@app.route("/")
def index():
    mars_dictionary = mongo.db.mars_dictionary.find_one()
    return render_template("index.html", mars_dictionary=mars_dictionary)



if __name__ == "__main__":
    app.run(debug=True)