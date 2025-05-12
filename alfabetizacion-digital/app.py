from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'clave-secreta'

# Crear base de datos si no existe
def init_db():
    if not os.path.exists('users.db'):
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )''')
            conn.commit()

init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()

            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash('Usuario o contraseña incorrectos.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect('users.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash('Usuario creado exitosamente. Ahora puedes iniciar sesión.')
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Este nombre de usuario ya está en uso.')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/clases')
def clases():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('clases.html', username=session['username'])

@app.route('/recursos')
def recursos():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('recursos.html', username=session['username'])

@app.route('/juegos')
def juegos():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('juegos.html', username=session['username'])

@app.route('/perfil')
def perfil():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('perfil.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
