from flask import *
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = os.urandom(16)
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ke_338.db' # database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # for better perfomance
db = SQLAlchemy(app)


# user data
class User:
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    ben_number = db.Column(db.Integer, nullable=False, unique=True)
    f_name = db.Column(db.String(50), nullable=False)
    s_name = db.Column(db.String(50), nullable=False)
    d_pic = db.Column(LargeBinary)


    def __repr__(self):
        return f'<User: {self.ben_number}>'
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
