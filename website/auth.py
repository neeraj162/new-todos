from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("floatingInput")
        password = request.form.get("floatingPassword")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Succesfully', category='success')
                login_user(user, remember=True)
                return redirect('/')
            else:
                flash('Incorrect Email/Password , try again...', category='error')
        else:
            flash('Email does not exist...', category='error')

    return render_template("login.html")

@auth.route("/sign-up", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("floatingInput")
        first_name = request.form.get("firstName")
        password1 = request.form.get("floatingPassword")
        password2 = request.form.get("floatingPassword1")
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists..',category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name)<2:
            flash('Your name must atleast have 2 characters', category='error')
        elif password1 !=password2:
            flash('Passwords does not match', category='error')
        elif len(password1)<7:
            flash('Password must atleast contain 7 characters', category='error')
        else:
            # good to go and add it to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            print(new_user)
            login_user(new_user, remember=True)
            flash("Account created Successfully..", category='success')
            return redirect('/')
               
    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')