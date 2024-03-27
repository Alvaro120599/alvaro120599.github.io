from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
app.debug = True

migrate = Migrate(app, db)

api = Api(app)


class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.id}>"

class Post(db.Model):
    id_post = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"))
    user = db.relationship("User", backref = "user")
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Post {self.id_post}>"

class Comment(db.Model):
    id_comment = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_post = db.Column(db.Integer, db.ForeignKey("post.id_post"))
    post = db.relationship("Post", backref = "post")
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Comment {self.id_comment}>"



class index(Resource):
    def get(self):
        all = Post.query.all()
        posts = []
        for post in all:
            n = {
                "id_post" : post.id_post,
                "post" : post.content
            }
            posts.append(n)
        return posts
    
class get_post_user(Resource):
    def post(self):
        user_data = request.get_json()
        user = User(name = user_data["name"])
        db.session.add(user)
        db.session.commit()
        return {
            "id_user" : user.id_user,
            "name" : user.name
        },201

    def get(self):
        all = User.query.all()
        users = []
        for user in all:
            n = {
                "id_user" : user.id_user,
                "name" : user.name
            }
            users.append(n)
        return users

class get_post_post(Resource):
    def get(self, id_user):
        all =Post.query.filter_by(id_user = id_user)
        post = []
        for n in all:
            post.append(
                {"content" : n.content}
            )
        return post

    def post(self, id_user):
        post_data = request.get_json()
        post = Post(id_user = id_user, content = post_data["content"])
        db.session.add(post)
        db.session.commit()
        return {
            "id_post" : post.id_post,
            "id_user" : post.id_user,
            "content" : post.content
        }

class update_delete_post(Resource):
    def put(self, id_user,id_post):
        post_data = request.get_json()
        post = Post.query.filter_by(id_post = id_post).first()
        if(post.id_user == id_user):
            post.content = post_data["content"]
            db.session.commit()
            return {
                "id_post" : id_post,
                "id_user" : id_user,
                "content" : post_data["content"]
            }
        else:
            return {"Error" : "Este Usuario No Puede Modificar Este Post"}
    
    def delete(self, id_user, id_post):
        post = Post.query.filter_by(id_post = id_post).first()
        if(post.id_user == id_user):
            db.session.delete(post)
            db.session.commit()
            return "Post Eliminado"
        else:
            return {"Error" : "Este Usuario No Puede Eliminar Este Post"}
        
class get_post_comment(Resource):
    def get(self, id_post):
        comments = Comment.query.filter_by(id_post = id_post)
        data = []
        for comment in comments:
            data.append({
                "comment" : comment.content
            })
        return data
    
    def post(self, id_post):
        if id_post in [x.id_post for x in Post.query.all()]:
            data_comment = request.get_json()
            comment = Comment(id_post = id_post, content = data_comment["content"])
            db.session.add(comment)
            db.session.commit()
            return {
                "id_post" : id_post,
                "comment" : data_comment["content"] 
            }
        else:
            return {"Error" : "Post No Existe"}



api.add_resource(index, '/')
api.add_resource(get_post_user, '/user')
api.add_resource(get_post_post, '/posts-by-user/<int:id_user>')
api.add_resource(update_delete_post,'/posts-by-user/<int:id_user>/<int:id_post>')
api.add_resource(get_post_comment, '/posts/comments/<int:id_post>')

if __name__ == '__main__':
    app.run(debug=True)