from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        flash('Registrasi sudah berhasil ! kamu bisa login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/phones', methods=['GET', 'POST'])
def manage_phones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM phones")
    phones = cur.fetchall()
    cur.close()
    return render_template('index.html', phones=phones)

@app.route('/add_hp', methods=['GET', 'POST'])
def add_hp():
    if request.method == 'POST':
        nama = request.form['nama']
        brand = request.form['brand']
        harga = request.form['harga']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO phones (nama, brand, harga) VALUES (%s, %s, %s)", (nama, brand, harga))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manage_phones'))
    return render_template('add_hp.html')

@app.route('/edit_hp/<int:id>', methods=['GET', 'POST'])
def edit_hp(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM phones WHERE id = %")