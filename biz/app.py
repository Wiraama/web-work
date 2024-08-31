# business backend
from flask import Flask, render_template, jsonify, abort, redirect, flash, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os, re, base64

app = Flask(__name__)
app.secret_key = os.urandom(16)
# setting up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biz0.db' # database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disabling track for better perfomance
db = SQLAlchemy(app)

# model - define structure of data
class Role(db.Model):
    __tablename__ = 'roles' # name of table

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)

    # spy to our class
    def __repr__(self):
        return '<Role %r>' % self.username


# now to the user class
class User(db.Model):
    # class to deal with the user
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# welcome home part
@app.route('/')
def home():
    # web has started we are on home page now
    products = Product.query.all()
    return render_template('home.html', products=products)


# let's login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # login part
    username = User.query.all()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            flash ('login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash ('Loging not successful', 'danger')
    #username = session.get('username', 'Guest')
    print(f"Username from session: {username}")
    return render_template('login.html', username=username)

# how about registering
@app.route('/register', methods=['GET', 'POST'])
def register():
    feedback = []
    # register part
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        
        if password != confirm_password:
            feedback.append("Password do not Match")
            return render_template('register.html', feedback=feedback)

        # password strength check
        conditions = [
                (r'[a-z]', "Atleast one lowercase"),
                (r'[A-Z]', "Atleast one uppercase"),
                (r'\d', "Atleast one number"),
                (r'[@$!%*?&#]', "Include at least one special character (@$!%*?&#)."),
                (r'.{8,}', "Atleast 8 characters long")
            ]

        # ensuring strong password is used
        if len(password) < 8:
            feedback.append("8+ characters")
        if not re.search(r'[A-Z]', password):
            feedback.append("Atleast one uppercase")
        if not re.search(r'[a-z]', password):
            feedback.append("Atleast one lowercase")
        if not re.search(r'[\d]', password):
            feedback.append("Atleast one digit")
        if not re.search(r'[!@#$%^&*()|<>{}:,.?]', password):
            feedback.append("Atleast one Special Charscter")

        if feedback:
            return render_template('register.html', feedback=feedback, username=username)
        
        else:
            flash("Weak Password...")


        if User.query.filter_by(username=username).first():
            flash('username already exist', 'danger')
            #return redirect(url_for('login'))
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('success registered', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


# product table
class Product(db.Model):
    __tablename = 'product'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    picture = db.Column(db.LargeBinary, nullable=False)
    video = db.Column(db.LargeBinary)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.item_name}>'

# Custom Jinja2 filter for Base64 encoding
@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')


# adding new product to database
@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        # add new item
        item_name = request.form['item_name']
        description = request.form['description']
        picture = request.files['picture'].read() # reads file as binary
        video = request.files['video'].read() 
        price = request.form['price']

        new_product = Product(
                item_name=item_name,
                description=description,
                picture=picture,
                video=video,
                price=price,
                )
        db.session.add(new_product)
        db.session.commit()
        
    # add all products from database
    products = Product.query.all()
    return render_template('add_product.html', products=products)
# lets return image request
@app.route('/image/<int:id>')
def image(id):
    product = Product.query.get(id)
    if product.picture:
        return Response(product.picture, mimetype='image/jpeg')
    return 'No image was found', 404


# lets return video request
@app.route('/video/<int:id>')
def video(id):
    product = Product.query.get(id)
    if product.video:
        return Response(product.video, mimetype='video/mp4')
    return 'No video was found', 404

# remove product by id
@app.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    if request.form.get('_method') == 'DELETE':
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            
            products = Product.query.all()
            return render_template('add_product.html', products=products)
# running our web
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creates all tables
    app.run(debug=True)
