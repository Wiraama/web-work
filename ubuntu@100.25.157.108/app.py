from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admins.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = os.urandom(8)
print(app.secret_key)

# data to the user
users = {}
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
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
            return redirect('register')

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
    
def add_user():
    if username.method == 'POST':
        username = request.form['username']
        password = requeat.form['password']
        
        # create new user
        new_user = User(username=username, password=passsword)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
