from flask import Flask, redirect,url_for, render_template, request
import random
app = Flask(__name__)

@app.route("/home")
@app.route("/")

def home():
	random_no=random.randint(0, 9)
	return render_template("home.html",random_no=random_no)

if __name__ == "__main__":
    app.run(debug=True)