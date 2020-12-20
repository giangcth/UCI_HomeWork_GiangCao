from flask import Flask, render_template, redirect, jsonify
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# setup mongo connection & connect to mongo db and collection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars = client.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars = client.db.mars
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    client.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)