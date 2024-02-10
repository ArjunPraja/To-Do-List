from pymongo import MongoClient
from flask import request, render_template

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')

# Select the database and collection
db = client['FlaskProject1']  # Replace 'FlaskProject1' with your actual database name
collection = db['todolist']  # Replace 'todolist' with your actual collection name

def home():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['abouttitle']
        days = request.form['days']
        
        # Insert the data into the collection
        data_to_insert = {
            "title": title,
            "description": description,
            "days": days
        }
        collection.insert_one(data_to_insert)
        
        # Render the home template (or any other template you want)
        return render_template('home.html')
