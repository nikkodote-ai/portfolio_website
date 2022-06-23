import os
from flask import Flask, render_template, request, url_for, redirect, flash, abort
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pickle
from forms import StrokeForm, CreateForm, RegisterForm, LoginForm
import numpy as np
import model_stroke
from datetime import datetime
from logging import FileHandler, WARNING


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), unique =True)
    subtitle = db.Column(db.String(250), unique =True)
    body= db.Column(db.String(250), unique =True)
    date_created = db.Column(db.Date)
    date_modified = db.Column(db.Date)
    img_url = db.Column(db.String(250), unique =True)
    post_url = db.Column(db.String(250), unique =True)
    tags = db.Column(db.String(250), unique =True)
    type = db.Column(db.String(250))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    def __repr__(self):
        return '<User: {}>'.format(self.id)


db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# for deleting posts
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function

@app.route('/')
def home():
    all_posts = Posts.query.all()
    return render_template('index.html', all_posts = all_posts)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/works')
def works():
    all_posts = Posts.query.all()
    return render_template('works.html', all_posts = all_posts)

@admin_only
@app.route('/create_post', methods = ['POST', 'GET'])
@login_required
def create_post():
    form = CreateForm()
    if form.validate_on_submit():
        new_post = Posts(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date_created = datetime.now(),
            date_modified = datetime.now(),
            img_url = form.img_url.data,
            post_url = form.post_url.data,
            tags = form.tags.data,
            type = form.type.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("create_post.html", form=form)

@app.route('/edit_post/<int:post_id>', methods = ['POST', 'GET'])
def edit_post(post_id):
    post= Posts.query.get(post_id)
    edit_form = CreateForm(
        title= post.title,
        subtitle= post.subtitle,
        body =  post.body,
        date_modified = post.date_modified,
        img_url = post.img_url,
        post_url = post.post_url,
        tags = post.tags,
        type = post.type
    )

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.body = edit_form.body.data
        post.date_modified = datetime.now()
        post.img_url = edit_form.img_url.data
        post.post_url = edit_form.post_url.data
        post.tags = edit_form.tags.data
        post.type = edit_form.type.data

        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_post.html', post = post, form=edit_form)

@app.route('/edit_post/<int:post_id>', methods = ['POST', 'GET'])
def delete_post(post_id):
    post_to_delete = Posts.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

#-----BLOG POST; Non-app technical writing----#
@app.route('/posts/<int:id>')
def posts(id):
    return render_template("blog_post.html")

#-----ML APPS hosted in the site----#
@app.route('/apps/stroke_prediction', methods = ['POST', 'GET'])
def stroke_app():
    # contain the following codes in if "model_name" statement
    model_stroke.make_pkl()
    model = pickle.load(open('model_stroke.pkl', 'rb'))
    form = StrokeForm()
    if request.method == "POST":
        #onehot code some of the answers because that is what the model requires
        gender_onehot = {choice[0]:0 for choice in form.gender.choices}
        gender_onehot[form.gender.data] = 1
        print(gender_onehot)
        worktype_onehot = {choice[0]:0 for choice in form.work_type.choices}
        worktype_onehot[form.work_type.data] = 1
        print(worktype_onehot)
        smoking_status_onehot = {choice[0]:0 for choice in form.smoking_status.choices}
        smoking_status_onehot[form.smoking_status.data] = 1
        print(smoking_status_onehot)
        # collate users answer
        form_answers = [[
            form.age.data, int(form.hypertension.data),
            int(form.heart_disease.data), int(form.ever_married.data),int(form.residence_type.data),
            form.avg_glucose_level.data, form.bmi.data,
            gender_onehot['female'], gender_onehot['male'], gender_onehot['other'],
            worktype_onehot['govt_job'], worktype_onehot['never_worked'], worktype_onehot['private'],
            worktype_onehot['self_employed'], worktype_onehot['children'],
            smoking_status_onehot['unknown'], smoking_status_onehot['formerly_smoked'],
            smoking_status_onehot['never_smoked'], smoking_status_onehot['smokes']]]
        form_answers_np = np.array(form_answers)
        prediction = model.predict(form_answers)

        return render_template("stroke_result.html", form=form, prediction=prediction)

    return render_template("stroke_post.html", form = form)


#-----LOGIN, REGISTRATION, AND AUTHENTICATION------#
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(name=form.name.data).first():
            print(User.query.filter_by(name=form.name.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, current_user=current_user)

#---LOGIN REQUIREMENTS AND VIEWS----#


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        user = User.query.filter_by(name=name).first()
        # Name doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()