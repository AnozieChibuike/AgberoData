from app import app,db
from app.api import otp, forgot
from flask_login import current_user, login_user, logout_user,login_required
from app.model import User
from werkzeug.urls import url_parse
from flask import render_template, request, redirect, flash, session, url_for, send_from_directory
import random


@app.route('/data',methods=['POST','GET'])
@login_required
def data():
    if request.method == 'POST':
        network = request.form.get('network_data')
        return network
    return render_template('data.html', )

@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html',users=users)

@app.route('/ads.txt')
def ads():
    return send_from_directory(app.static_folder, 'ads.txt')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    message = session.pop('created',None)
    if current_user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(request.form.get('remember') == 'y')
        if user is None or not user.check_password(password):
            flash('Invalid login details')
            return redirect(url_for('login'))
        if request.form.get('remember') == 'y':
            print(request.form.get('remember'))
            login_user(user,remember=True)
        else:
            login_user(user,remember=False)
        next_page = request.args.get('next')
        session['welcome'] = f'User: {current_user.fullname}'
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html',message=message)

@app.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    message = session.get('welcome',None)
    return render_template('dashboard.html',message=message)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        name = f"{request.form['firstname'].capitalize()} {request.form['lastname'].capitalize()}"
        email = request.form['email']
        password = request.form['password']
        if password == request.form['passwordrepeat'] and len(password) >= 8:
            if User.query.filter_by(email=email).first() is None:
                otp1 = random.randint(1000, 9999)
                if otp(name, email, otp1):
                    print('SendingOtp')
                    session['otp'] = 'Otp sent to email address'
                    db.session.add(User(otp=otp1))
                    db.session.commit()
                    return redirect(url_for('verify',name=name,email=email,password=password))
            elif User.query.filter_by(email=email).first() is not None:
                flash('email already taken')
                return redirect('/signup')
        elif len(password) < 8:
            flash('Password too short')
            return redirect('/signup')
        elif password != request.form['passwordrepeat']:
            flash('Password don\'t match')
            return redirect('/signup')
    return render_template('signup.html')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')
    message = session.pop('otp',None)
    if email == None:
        return redirect('/signup')
    if request.method == 'POST':
        otp2 = f"{request.form['0']}{request.form['1']}{request.form['2']}{request.form['3']}"
        print(otp2)
        if User.query.filter_by(otp=otp2) is not None:
            session['created'] = 'Account successfully created, Login!'
            user = User(fullname=name,email=email)
            user.set_password(password)
            db.session.add(user)
            User.query.filter_by(otp=otp2).delete()
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Invalid Otp')
    return render_template('verify.html',message=message,email=email)

@app.route('/pricing')
def pricing():
    return render_template('index.html')

@app.route('/forgot-password',methods=['POST','GET'])
def forget():
    if request.method == 'POST':
        email = request.form['email']
        if User.query.filter_by(email=email) is not None:
            otp1 = random.randint(1000, 9999)
            if forgot('customer', email, otp1):
                session['otp'] = 'Otp sent to email address'
                db.session.add(User(otp=otp1))
                db.session.commit()
                return redirect(url_for('new',email=email))
            else:
                flash('Something went wrong')
                return redirect(url_for('forget'))
        else:
            flash('No record with this email found')
            return redirect(url_for('forget'))
    return render_template('forget.html')

@app.route("/account")
@login_required
def account():
    user = current_user
    return render_template('account.html')


@app.route("/new-password", methods=['POST', 'GET'])
def new():
    email = request.args.get('email')
    if email == None:
        return redirect(url_for('login'))
    message = session.pop('otp',None)
    if request.method == 'POST':
        otp2 = request.form['otp']
        password = request.form['password']
        print(otp2)
        if password == request.form['confirm-password']:
            if User.query.filter_by(otp=otp2) is not None:
                session['created'] = 'Password reset successfully'
                user = User.query.filter_by(email=email).first()
                user.set_password(password)
                db.session.commit()
                return redirect('/login')
            else:
                flash('Invalid Otp')
        else:
            flash('Password don\'t match')

    return render_template('new.html',message=message)