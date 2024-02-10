from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['FlaskProject1']  # Replace 'FlaskProject1' with your actual database name
todo_collection = db['todolist']  # Replace 'todolist' with your actual collection name
login_collection = db['login']  # Replace 'login' with your actual collection name


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/create-todo', methods=["GET", "POST"])
def create_todo():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        days = request.form.get("days")

        # Insert the todo item into the database
        todo_collection.insert_one({'title': title, 'description': description, 'days': days})

        return redirect(url_for('view_list'))
    else:
        return render_template('create_todo.html')


@app.route('/view-list')
def view_list():
    # Fetch all todo items from the collection
    todo_list = todo_collection.find()

    return render_template('viewlist.html', todo_list=todo_list)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/deleteNumber", methods=["POST"])
def deleteNumber():
    if request.method == "POST":
        index_to_delete = int(request.form.get("delnumber"))-1

        # Fetch all documents in the collection
        all_documents = list(todo_collection.find())

        # Ensure that the index to delete is within the bounds of the collection
        if 0 <= index_to_delete < len(all_documents):
            document_to_delete = all_documents[index_to_delete]
            todo_collection.delete_one(document_to_delete)  # Delete the document at the specified index

    return redirect(url_for('view_list'))


@app.route("/profile", methods=['POST'])
def profile():
    return render_template('profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user with the provided email and password exists in the database
        user = login_collection.find_one({'username': email, 'password': password})

        if user:
            # User found, redirect to home page or dashboard
            return redirect(url_for('home'))
        else:
            # User not found, redirect back to login page
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
    


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user with the provided email already exists in the database
        existing_user = login_collection.find_one({'username': email})

        if existing_user:
            # User already exists, redirect to login page
            return redirect(url_for('login'))
        else:
            # User does not exist, insert the new user into the database
            login_collection.insert_one({'name': name, 'username': email, 'password': password})

            # Redirect to the login page after successful registration
            return redirect(url_for('login'))
    else:
        return render_template("register.html")
    
@app.route('/<path:undefined_path>')
def catch_all(undefined_path):
    return f'<h1>Page not found for: {undefined_path}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
