import peeweedbevolve
from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for
from models.user import User
from flask_login import current_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')
    # display form


@users_blueprint.route('/', methods=['POST'])
def create():
    user_name = request.form.get("user_name")
    user_email = request.form.get("user_email")
    user_password = request.form.get("user_password")

    user = User(name=user_name, email=user_email, password=user_password)

    if user.save():
        flash("User Created")
        return redirect(url_for("users.new"))

    else:
        for error in user.errors:
            flash(error)
        # linking and displaying at the specific file
        return render_template("users/new.html")


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass
# display single user


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"
# display all users


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    # Query for a user
    flash("User edited")
    user = User.get_or_none(User.id == id)
    # Render a template and pass the user out
    return render_template('users/edit.html', user=user, id=id)
# edit users details


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
# funtion to update details
