import time

from fileStorage import app

from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_login import login_user,login_required,logout_user
from fileStorage.models import User
from fileStorage import db


@app.route('/')
def index():
    return render_template("public/index.html")


@app.route("/sign-up",methods=["GET","POST"])
def sign_up():

    if request.method == "POST":
        
        new_user = User(
            username = request.form["username"],
            email = request.form["email"],
            password = request.form["password"]
        )

        users = User.query.filter_by(email =new_user.email).all()
        if len(users) > 0:
            return redirect(request.url)

        db.session.add(new_user)
        db.session.commit()

        return redirect(request.url)

    return render_template("public/sign_up.html")


@app.route("/login",methods=["GET","POST"])
def login():

    if request.method == "POST":
        password = request.form["password"]

        user = User.query.filter_by(username = request.form["username"]).first()
        if not user or not password == user.password:
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))

    return render_template("public/login.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile/files")
@login_required
def showFiles():
    return render_template("/public/profiles/files.html")


@app.route("/profile/upload-file",methods=["POST"])
@login_required
def upload_file():
    if request.method=="POST":
        file_size = request.cookies.get("filesize")

        file = request.files["file"]
        print(f"FileSize: {file_size}")
        res = make_response(jsonify({'message':f"{file.filename} uploaded"}), 200)
        return res
    return redirect(url_for('showFiles'))