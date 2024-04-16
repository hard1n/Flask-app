from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.db_models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os

# FAKE POSTS TO RENDER
posts = [
  {
    "title": "Blog Post #1",
    "author": "John Doe",
    "content": "Testing post #1",
    "date_posted": "21 feb 2024"
  },
  {
    "title": "Blog Post #2",
    "author": "Jane Doe",
    "content": "Testing post #2",
    "date_posted": "21 feb 2024"
  }
]

@app.route("/home")
@app.route("/")
def home():
  return render_template("home.html", posts=posts)

@app.route("/about")
def about():
  return render_template("about.html", title='About')

@app.route("/register", methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
    
  form = RegistrationForm()
  if form.validate_on_submit():
    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    new_user = User(username=form.username.data, email=form.email.data, password=pw_hash)
    db.session.add(new_user)
    db.session.commit()
    flash(f'Account created succesfully!', 'success')
    return redirect(url_for('login'))
  return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  
  form = LoginForm()
  if form.validate_on_submit():
    # Gettin User from DB by email
    user = User.query.filter_by(email=form.email.data).first()
    
    # if form.email.data == 'admin@gmail.com' and form.password.data == 'passw':
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      # flash('Welcome back!', 'success')
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Check Email and Password', 'danger')
  return render_template("login.html", title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('home'))

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
  form_picture.save(picture_path)

  return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      file_name = save_picture(form.picture.data)
      current_user.image_file = file_name
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Information updated succesfully!', 'success')
    redirect(url_for('profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  user_image = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template("profile.html", title="Profile" , user_image=user_image, form=form)