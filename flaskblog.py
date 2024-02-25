from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# config values of the app
app.config['SECRET_KEY'] = 'cf6c0c0039ad00a386c898d6c6e773c2'

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
  form = RegistrationForm()
  if form.validate_on_submit():
    flash(f'User {form.username.data} registered!', 'success')
    return redirect(url_for('home'))
  return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@gmail.com' and form.password.data == 'passw':
      flash('Welcome back!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Check Username and Password', 'danger')
  return render_template("login.html", title='Login', form=form)

# Debugging 
if __name__ == "__main__":
  app.run(debug=True)