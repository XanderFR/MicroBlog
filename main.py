import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB database
client = MongoClient("mongodb://localhost:#####")
app.db = client.microblog


@app.route('/', methods=["GET", "POST"])  # Function to recieve POST requests
def home():
    # Takes data from microblog form and inserts it into the MongoDB database
    if request.method == "POST":  # If microblog form makes a POST request
        entryContent = request.form.get("content")  # Take the microblog content
        formattedDate = datetime.datetime.today().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entryContent, "date": formattedDate})  # Put data into MongoDB

    # Reformat text content and date
    entriesWithDate = [
        (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b-%d")
        )
        for entry in app.db.entries.find({})  # For loop that goes through MongoDB data
    ]

    return render_template('./home.html', entries=entriesWithDate)

if __name__ == "__main__":
    app.run(debug=True)
