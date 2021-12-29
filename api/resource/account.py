import random

from flask import make_response, render_template, redirect, url_for
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, logout_user
from flask_restful import Resource
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, current_user
import os
import json
from api.resource import status

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])

class Login(Resource):
    def get(self):
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect("/")

            return '<h1>Invalid username or password</h1>'
            #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

        return make_response(render_template('login.html', form=form))

    def post(self):
        return self.get()

class Signup(Resource):
    def get(self):
        form = RegisterForm()
        status_code = 0

        if form.validate_on_submit():
            # check database if same user name/email exists
            user = User.query.filter_by(username=form.username.data).first()
            email = User.query.filter_by(email=form.email.data).first()
            if user:
                status_code = 1
            elif email:
                status_code = 2
            else:
                hashed_password = generate_password_hash(form.password.data, method='sha256')
                new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                avatar_index = random.randrange(10) + 1
                if os.path.exists('./static/json/user_data.json'):
                    with open("./static/json/user_data.json", 'r+') as json_fp:
                        data = json.load(json_fp)
                        data['user'].append({
                            'id': new_user.id,
                            'name': new_user.username,
                            'avatar': avatar_index
                        })
                        json_fp.seek(0, 0)
                        json.dump(data, json_fp)
                else:
                    data = {}
                    data['user'] = []
                    data['user'].append({
                        'id': new_user.id,
                        'name': new_user.username,
                        'avatar': avatar_index
                    })
                    with open('./static/json/user_data.json', 'w') as json_fp:
                        json.dump(data, json_fp)

                return '<h1>New user has been created!</h1>'
            #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

        return make_response(render_template('signup.html', form=form, status_code=status_code))

    def post(self):
        return self.get()

class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect('/')

    def post(self):
        return self.get()