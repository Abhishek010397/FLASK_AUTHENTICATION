from flask import render_template, url_for, redirect, flash, session, request
from flaskacl import app, db, bcrypt
from flaskacl.forms import LoginForm, RegistrationForm, UpdateForm
from flaskacl.models import User
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        missing = User.query.filter_by(username=form.username.data).first()
        if missing is None:
            flash('User Not Registered')
        else:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session.permanent = True
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful, Please Check Your Password')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.role == 'admin':
        return redirect(url_for('logout'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #create hashed password for new generated user
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful!!')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if not current_user.role == 'user':
        return render_template('logout')
    form = UpdateForm()
    user_id = current_user.id
    assigned_role = current_user.role
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            if form.submit():
                username = form.username.data
                password = bcrypt.generate_password_hash(form.password.data)
                update_user = User(id=user_id, username=username,
                                   password=password, role=assigned_role)
                db.session.add(update_user)
                db.session.commit()
                flash('Update Successful!!')
                return redirect(url_for('logout'))

    return render_template('update.html', form=form)


@app.route('/all')
def retrieveuserlist():
    if current_user.role == 'admin':
        users = User.query.all()
        return render_template('user.html', users=users)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not current_user.role == 'admin':
        return redirect(url_for('logout'))
    user = User.query.filter_by(id=id).first()
    user_password = user.password
    form = UpdateForm()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            if form.submit():
                username = request.form['name']
                password = request.form['password']
                if password == user_password:
                    print('Matched')
                    role = form.role.data
                    updated_user = User(
                        id=id, username=username, password=password, role=role)
                    db.session.add(updated_user)
                    db.session.commit()
                    flash("User Has Been Updated")
                    return redirect(f'/edit/{id}')
                else:
                    print('Unmatched')
                    role = form.role.data
                    updated_user = User(
                        id=id, username=username, password=bcrypt.generate_password_hash(password), role=role)
                    db.session.add(updated_user)
                    db.session.commit()
                    flash("User Has Been Updated")
                    return redirect(f'/edit/{id}')
    return render_template('edit.html', form=form, user=user)


@app.route('/delete/<int:id>')
def delete(id):
    if not current_user.role == 'admin':
        return redirect(url_for('logout'))
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User Has Been Deleted')
    return redirect(url_for('retrieveuserlist'))
