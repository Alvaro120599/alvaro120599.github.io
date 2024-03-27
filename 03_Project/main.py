from flask import Flask, render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")


users_data = [{
    "name": "cristhian",
    "age": 34,
    "language": "python",
}, {
    "name": "genaro",
    "age": 34,
    "language": "nodejs",
}]
    

@app.route('/users')
def users():
    return render_template("users.html", users=users_data)
# SELECT * FROM USERS

@app.route('/users/<name>')
def users_by_name(name):
    user = {}
    for user_data in users_data:
        if user_data.get("name") == name:
            user = user_data
    return render_template("user.html", user=user)
# SELECT * FROM USERS where name={{name}}

# @app.route('/users-add/')  # POST
# INSERT INTO USERS VALUES ('name', 'age', 'language')

# @app.route('/users/ID/change')  # UPDATE
# UPDATE USERS WHERE SET name={{name}}

# @app.route('/users/ID/delete')  # DLETE
# DELETE
