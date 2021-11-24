from flaskacl import *
from flaskacl.models import *

db.create_all()
user1=User(username='Admin',password=bcrypt.generate_password_hash('Admin'),role='admin')
db.session.add(user1)
db.session.commit()

