from flask import Flask
from markupsafe import escape
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/messages/')
def messages():
    return []

@app.route('/messages-in-dashboard/')
def messages_in_dashboard():
    return []

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


data = [{
    "user": "cristhian",
    "password": 123456,
}, {
    "user": "genaro",
    "password": 12345678,
}]

# GET /dashboard/ => {}
# POST > {} => view
# PUT
# PATCH
# DELETE

# /login 
# 
# application/json
#

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data_input = request.get_json()
        user = data_input["user"]
        password = data_input["password"]
        if user and password:
            for i in data:
                if i.get("user") == user and str(i.get("password")) == password:
                    return "valid login"
            return "Invalid login"
        else:
            return "Invalid login"
    else:
        return "You need to login"


