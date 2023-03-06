from fileStorage import app
from fileStorage.File import File, get_user_file_name, get_file
from fileStorage.models import User
from fileStorage import db

from flask import render_template, request, redirect, url_for, make_response, jsonify, send_from_directory, send_file
from flask_login import login_user,login_required,logout_user,current_user


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('show_user_files'))
    else:
        return redirect(url_for('login'))


@app.route("/sign-up",methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        new_user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"]
        )

        users = User.query.filter_by(email =new_user.email).all()
        if len(users) > 0:
            return redirect(request.url)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("public/sign_up.html")


@app.route("/login",methods=["GET","POST"])
def login():

    if request.method == "POST":
        password = request.form["password"]

        user = User.query.filter_by(username = request.form["username"]).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('index'))
        return redirect(url_for('login'))

    return render_template("public/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile/files")
@login_required
def show_user_files():
    return render_template("/public/profiles/files.html", files=File.show_user_files(current_user))


@app.route("/profile/upload-file",methods=["POST"])
@login_required
def upload_file():

    if request.method=="POST":

        file = File(request.files["file"],current_user)
        file.save()

        res = make_response(jsonify({
            'message': f"{file} uploaded",
            'folderId': file.get_folder_id(),
        }), 200)

        return res

    return redirect(url_for('show_user_files'))


@app.route("/profile/delete-file/<folder_id>",methods=["POST"])
@login_required
def delete_file(folder_id):

    if request.method == "POST":

        file_name = get_user_file_name(current_user, folder_id)
        File.delete(current_user,folder_id)

        res = make_response(jsonify({
            'message': f"{file_name} deleted",
        }), 200)
        return res

    return redirect(url_for('show_user_files'))


@app.route("/profile/download-file/<folder_id>",methods=["GET"])
@login_required
def download_file(folder_id):
    if request.method=="GET":

        file_directory = get_file(current_user,folder_id)

        return send_file(file_directory, as_attachment=True)

    return redirect(url_for('show_user_files'))