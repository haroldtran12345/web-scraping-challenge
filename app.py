from flask import Flask, render_template, redirect
# import pymongo
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.mars_app


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_data= mongo.db.mars_data
# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", data=destination_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    
    my_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, my_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)