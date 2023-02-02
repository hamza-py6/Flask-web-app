from flask import Blueprint, flash,render_template, request, redirect, url_for
from project.models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from . import db
#import flask
auth = Blueprint('auth',__name__)


@auth.route('/',methods=['GET','POST'])
def home():
    if login_user:
        return redirect(url_for('views.notes'))
    return redirect(url_for('auth.sign_up'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('passwd1')
        password2 = request.form.get('passwd2')
        #
        user = User.query.filter_by(email=email).first()
        if user:
            flash('user alredy exict',category='error')
        elif len(email) < 3:
            flash('email must be more than 4 characters',category='error')
        elif len(password1) < 3:
            flash ('password must be more than 4 characters',category='error')
        elif password1 != password2:
            flash('password don\'t match ',category='error')
        else:
            new_user = User(email=email,first_name=first_name,password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!', category='info')
            return redirect(url_for('views.notes'))

    return render_template('sign_up.html',user=current_user)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('passwd1')
        
        #VVVVVVVVVVVVV---- IMPORTANT ----VVVVVVVVVVVVV
        user = User.query.filter_by(email=email).first()
        #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        if user :
            if check_password_hash(user.password,password):
                flash('logged in successfully !',category='info')
                login_user(user,remember=True)
                return redirect(url_for('views.notes'))
            else:
                flash('incorect password try again',category='error')
        else:
            flash('email does not exist',category='error')
    
    return render_template('login.html',user = current_user)


@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))