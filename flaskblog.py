from flask import Flask, render_template

app = Flask(__name__)

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
  # return "<h1>HOME</h1>"
  return render_template("home.html", posts=posts)

@app.route("/about")
def about():
  # return "<h1>HOME</h1>"
  return render_template("about.html", title="About")

if __name__ == "__main__":
  app.run(debug=True)