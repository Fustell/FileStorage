from fileStorage import app
from fileStorage.models import User
from flask import render_template


@app.route('/admin/dashboard')
def admin_dashboard():
    users = User.query.all()
    return render_template("admin/dashboard.html", users = users)

@app.route('/admin/profiles')
def admin_profiles():
    return "profiles"
