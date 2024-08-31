from app import db, User, app

with app.app_context():
    # Query all users
    users = User.query.all()

    # Print out the users
    for user in users:
        print(f"Username: {user.username}, Password Hash: {user.password}")
