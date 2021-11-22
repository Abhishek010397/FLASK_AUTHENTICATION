import functools
from flask import render_template,url_for,redirect, flash, abort
from flaskacl import app, db, bcrypt
from flaskacl.forms import LoginForm,RegistrationForm
from flaskacl.models import User
from flask_login import login_user, login_required, logout_user,current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        #create hashed password for new generated user
        hashed_password= bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your Account is created! Login to Continue')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# def admin(user):
#     existing_user=User.query.filter_by(username='Admin').first()
#     print(user.id)
#     print(current_user.id)
#     if user.id == existing_user.id:
#         print(user.username)

@app.route('/role')
def role():
    return render_template('amazon.html')


def roles():
    user= User.query.filter_by(username='Admin').first()
    user

