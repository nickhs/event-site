from flask import request, Blueprint, redirect, render_template
from flask.ext.login import LoginManager, login_user
from models import Owner

auth = Blueprint('auth', 'eventsite')

login_manager = LoginManager()

login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(userid):
    return Owner.query.get(userid)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST' and request.form:

        user = Owner.query.filter_by(name=request.form['name']).first()

        if user.password != request.form['password']:
            return 'Unauthorized', 401

        # Log the user in.
        login_user(user)

        return redirect('/admin/eventview')
    return render_template("login.html")
