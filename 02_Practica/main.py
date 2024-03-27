from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
app.debug = True

migrate = Migrate(app, db)


class Usuario(db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.Text, nullable = False)
    contraseña = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.id}>"
    

class Post(db.Model):
    id_post = db.Column(db.Integer, primary_key = True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey("usuario.id_user"))
    user = db.relationship("Usuario", backref = "user")
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Post {self.id_post}>"
    
class Comentarios(db.Model):
    id_comentario = db.Column(db.Integer, primary_key = True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("post.id_post"))
    post = db.relationship("Post", backref = "post")
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Comentario {self.id_comentario}>"    
    



@app.route('/')
def index():
    post = Post.query.all()
    comentarios = Comentarios.query.all()
    usuarios = Usuario.query.all()
    return render_template('index-nl.html', post = post, comentarios = comentarios, usuarios = usuarios)


@app.route('/usuario/<int:id_user>', methods = ['GET', 'POST'])
def index_user(id_user):
    if request.method == 'GET':
        post = Post.query.all()
        comentarios = Comentarios.query.all()
        usuarios = Usuario.query.all()
        return render_template('index.html', post = post, comentarios = comentarios, id = id_user, usuarios = usuarios)
    if request.method == 'POST':
        return redirect(url_for('cerrar_sesion', user_id = id_user))


@app.route('/log-in', methods = ['GET', 'POST'])
def iniciar_sesion():
     if(request.method == 'GET'):
        return render_template('log-in.html')
     if(request.method == 'POST'):
        usuarios = Usuario.query.all()
        for user in usuarios:
            if request.form["usuario"] == user.usuario and request.form["contraseña"] == user.contraseña:
                return redirect(url_for('index_user', id_user = user.id_user))        
        error = "Usuario o Contraseña Incorrecta"
        return render_template('log-in.html', error = error)
     

@app.route('/cerrarsesion/<int:user_id>', methods = ['GET', 'POST'])
def cerrar_sesion(user_id):
    if request.method == 'GET':
        return render_template('cerrar-sesion.html', id = user_id)
    if request.method == 'POST':
        return redirect(url_for('index'))


@app.route('/sign-up', methods = ['GET', 'POST']) 
def crear_usuario():
    if(request.method == 'GET'):
        return render_template('sign-up.html')
    if(request.method == 'POST'):
        usuarios = Usuario.query.all()
        for user in usuarios:
            if request.form["usuario"] == user.usuario:
                error = "Usuario Ya Existe"
                return render_template("sign-up.html", error = error)                
        user = Usuario(usuario = request.form["usuario"], contraseña = request.form["contraseña"])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index_user', id_user = user.id_user))




@app.route('/mi-muro/<int:id>', methods = ['GET', 'POST'])
def usuario_muro(id):
    if request.method == 'GET':
        post = Post.query.filter_by(id_user = id).all()
        comentarios = Comentarios.query.all()
        return render_template('usuario-muro.html', post = post, comentarios = comentarios, id = id)
    if request.method == 'POST':
        return redirect(url_for('crear_post', id_user = id))
    

@app.route('/mi-muro/delete/<int:id_post>', methods = ['GET','POST'])
def delete_post(id_post):
    post = Post.query.filter_by(id_post = id_post).first()
    if request.method == 'GET':
        return render_template('delete-post.html', post = post)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('usuario_muro', id = post.id_user))
    
    

@app.route('/mi-muro/post/agregar/<int:id_user>', methods = ['GET', 'POST'])
def crear_post(id_user):
    if request.method == 'GET':
        return render_template('add-post.html', id = id_user)
    if request.method == 'POST':
        post = Post(id_user = id_user, content = request.form['post'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('usuario_muro', id = id_user))


@app.route('/comentar/<int:id_post>', methods = ['GET', 'POST'])
@app.route('/comentar/<int:id_post>/<int:id_user>', methods = ['GET', 'POST'])
def comentar(id_post, id_user = None):
    if request.method == 'GET':
        return render_template('add-comment.html')
    if request.method == 'POST':
        if  id_user == None:
            comentario = Comentarios(id_post = id_post, content = request.form['comentario'])
            db.session.add(comentario)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            comentario = Comentarios(id_post = id_post, content = request.form['comentario'])
            db.session.add(comentario)
            db.session.commit()
            return redirect(url_for('index_user', id_user = id_user))   
    
@app.route('/editarpost/<int:id_post>', methods = ['GET', 'POST'])
def editar(id_post):
    post = Post.query.filter_by(id_post = id_post).first()
    if request.method == 'GET':
        return render_template('edit-post.html', post = post.content)
    if request.method == 'POST':
        post.content = request.form["post"]
        db.session.commit()
        return redirect(url_for('usuario_muro', id = post.id_user))







     







    


    
