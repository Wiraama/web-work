from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.secret_key = os.urandom(8)
print(app.secret_key)

# data to the user
users = {}

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    """ the render_template help to link with html files """
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Logged successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid details, proceed to register kindly', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('username taken', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            users[username] = {'password': hashed_password}
            flash('registered successfuly', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
