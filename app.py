from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'e-parkir'

mysql = MySQL(app)

@app.route('/')
def index():
    session.clear()
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM akun WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password_hash(user[3], password):  # Menggunakan indeks yang benar untuk password hash
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO akun (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cursor.close()
        flash('You are now registered and can log in')
        return redirect(url_for('index'))  # Redirect to login page after successful registration
    return render_template('register.html')  # Render the registration page for GET request

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')  # Menggunakan template dashboard.html
    return redirect(url_for('index'))

@app.route('/barcard')
def barcard():
    if 'username' in session:
        return render_template('normal-table.html')  # Menggunakan template dashboard.html
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
