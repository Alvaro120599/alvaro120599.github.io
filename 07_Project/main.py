from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

ma = Marshmallow(app)

db = SQLAlchemy(app)
app.debug = True

migrate = Migrate(app, db)

api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.id}>"
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return f"<Message {self.id}>"


class UserBasicSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = User


user_basic_schema = UserBasicSchema()
users_basic_schema = UserBasicSchema(many = True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "age", "created_at")
        model = User
        datetimeformat = "%Y-%m-%d-%H:%M"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class WorkingResource(Resource):
    def get(self):
        return {"working": True}


class MessageSchema(ma.Schema):
    user = ma.Nested(UserSchema)
    class Meta:
        fields = ("id", "content", "created_at", "user")
        model = Message
        datetimeformat = "%Y-%m-%d-%H:%M"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)

class PublicUserResource(Resource):
    def get(self):
        users_data = User.query.all()
        return users_basic_schema.dump(users_data)
    

class MessagesByUserResource(Resource):

    def get(self, user_id):
        messages_data = Message.query.filter_by(user_id = user_id).all()
        return messages_schema.dump(messages_data)


class UserResource(Resource):
    def get(self):
        users_data = User.query.all()
        return users_schema.dump(users_data)
    
    def post(self):
        data_user = request.get_json()
        user = User(**data_user)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


class UserByIDResource(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id = user_id).first()
        return user_schema.dump(user)

    def patch(self, user_id):
        data_user = request.get_json()
        user = User.query.filter_by(id = user_id).first()
        user.name = data_user["name"]
        db.session.commit()
        return user_schema.dump(user), 201

    def delete(self, user_id):
        user = User.query.filter_by(id = user_id).first()
        db.session.delete(user)
        db.session.commit()
        return {}, 204


api.add_resource(WorkingResource, '/')
api.add_resource(PublicUserResource, '/public/users')
api.add_resource(UserResource, '/users')
api.add_resource(UserByIDResource, '/users/<int:user_id>')
api.add_resource(MessagesByUserResource, '/messages-by-user/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True)
