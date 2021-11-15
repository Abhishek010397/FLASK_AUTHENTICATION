from flaskacl import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#create table
class User(db.Model,UserMixin):
    #create columns
    id = db.Column(db.Integer,primary_key=True)
    username  = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)