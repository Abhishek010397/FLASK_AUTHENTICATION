from flaskacl import db, login_manager
from flask_authorize import RestrictionsMixin,AllowancesMixin,PermissionsMixin
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#mapping tables
UserGroup= db.Table(
    'user_group',db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id',db.Integer, db.ForeignKey('groups.id'))
)

UserRole = db.Table(
    'users_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)
#create table
class User(db.Model,UserMixin):

    __tablename__ = 'users'
    #create columns
    id = db.Column(db.Integer,primary_key=True)
    username  = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)
    roles = db.relationship('Role',secondary=UserRole)
    groups=db.relationship('Group',secondary=UserGroup)

#create table
class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

#create table
class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)



