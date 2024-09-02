from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Intializing
db = SQLAlchemy(app)

# model defition
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # defining string representation
    def __repr__(self):
        return f'<User {self.username}>'

# creating database and tables
# @app.before_first_request
def create_table():
    db.create_all()


# define route('/')
@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
       username = request.form['username']
       email = request.form['email']
        
       # Create a new User instance
       new_user = User(username=username, email=email)
        
       # Add the new user to the database
       db.session.add(new_user)
       db.session.commit()
        
        # Redirect to the home page
       return redirect(url_for('home'))
    
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
