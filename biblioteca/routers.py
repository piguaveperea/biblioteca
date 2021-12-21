from sqlalchemy import or_
from biblioteca import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from biblioteca.models import Biblioteca, Libro, Rol, Usuario, Computadora
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from uuid import uuid4
@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.filter_by(id=usuario_id).first()


@app.errorhandler(404)
def NoFoundpage(err):
    return render_template('404.html')

@app.route('/')
@app.route('/home')
def Home():
    bibliotecas = Biblioteca.query.all()
    libros = Libro.query.all()
    return render_template('index.html', bibliotecas=bibliotecas, libros=libros)


@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    rol = Rol.query.filter_by(tipo='Anonimo').first()
    form = request.form
    if request.method == 'POST':
        ci = form['ci']
        nombre = form['nombre']
        apellido = form['apellido']
        correo = form['correo']
        clave = generate_password_hash(form['clave'])


        usuario = Usuario.query.filter_by(ci=ci).first()
        if usuario:
            flash('El usuario ya posse una cuenta')
        if not usuario:
            usuario = Usuario.query.filter_by(correo=correo).first()
            if usuario:
                flash('El correo esta en uso')
            else:
                try:
                    usuario = Usuario(ci=ci, nombre=nombre, apellido=apellido,correo=correo, clave=clave, id_rol=rol.id, id_publico=uuid4())        
                    db.session.add(usuario) 
                    db.session.commit()
                    flash("Usuario creado correctamente")
                    return redirect(url_for('Home'))
                except:
                    flash("usuario no creado")

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def SignIn():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = request.form
    if request.method == 'POST':
        usuario = form['usuario']
        clave = form['clave']
        n_usuario = Usuario.query.filter_by(ci=usuario).first()
        if n_usuario:
            if check_password_hash(n_usuario.clave, clave):
                login_user(n_usuario)
                return redirect(url_for('Profile', public_id= n_usuario.id_publico ))
            else:
                print('clave incorrecta')
        if not n_usuario:
            n_usuario = Usuario.query.filter_by(correo=usuario).first()
            if n_usuario:
                if check_password_hash(n_usuario.clave, clave):
                    return redirect(url_for('Home'))
                else:
                    print('contraseña incorecta')
            else:
                flash('usuario no existe')

    return render_template('signin.html')

@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('SignIn'))


@app.route('/profile/<public_id>')
def Profile(public_id):
    computadora = Computadora.query.filter_by(id_usuario=current_user.id).first()
    libros = Libro.query.filter_by(id_usuario = current_user.id).all()
    return render_template('user/index.html', libros=libros, computadora= computadora)

@app.route('/profile/setting')
def Setting():
    return "hola"


@app.route('/take_book/<id_book>', methods=['GET', 'POST'])
def TakeBook(id_book):
    if current_user.is_authenticated:
        libro = Libro.query.filter_by(id=id_book).first()
        if request.method == 'POST':
            libro.id_usuario = current_user.id 
            libro.ocupado = True
            db.session.commit()
            return redirect(url_for('Profile', public_id=current_user.id_publico))  
    else:
        return redirect(url_for('SignIn'))
    return render_template('user/book.html', id_book=id_book, libro=libro)

@app.route('/quit_book/<id_book>', methods=['GET', 'POST'])
def QuitBook(id_book):
    if current_user.is_authenticated:
        libro = Libro.query.filter_by(id = id_book).first()
        if  libro.id_usuario == current_user.id:
            libro.id_usuario = None
            libro.ocupado = False
            db.session.commit()
            return redirect(url_for('Profile', public_id= current_user.id_publico ))
        else:
            flash("usted no pudes delvover ese libro")
    else: 
        return redirect(url_for('Home'))


@app.route('/detail_book/<id_book>')
def DetailBook(id_book):
    libro = Libro.query.filter_by(id=id_book).first()
    return render_template ('detail_book.html', libro = libro)

@app.route('/book', methods=['GET', 'POST'])
def Books():
    libros = []
    if request.method == 'POST':
        text = request.form['book']
        search_book = "%{}%".format(text) 
        libros =  db.session.query(Libro).filter(or_(Libro.titulo.like(search_book),Libro.autor == text )).all()
        if not libros: 
            flash("hola")
        return render_template('books.html', libros = libros)
    
    return render_template('books.html', libros = libros)

