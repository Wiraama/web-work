from flask import Flask, render_template, request, redirect, url_for, flash
import os


app = Flask(__name__)
app.secret_key = os.urandom(8)
print(app.secret_key)

# data to the user
users = {}

@app.route('/')
def home():
    """ the render_template help to link with html files """
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            flash('Logged successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid details', 'danger')
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('username taken', 'danger')
        else:
            users[username] = {'password': password}
            flash('registered successfuly', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')
if __name__ == '__main__':
    app.run(debug=True)
