import peeweedbevolve
from flask import Flask, render_template, request, flash, Blueprint
from models.user import User

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

    try:
        user.save()
        # flash(f"Saved store:{store_name}")
        return redirect(url_for("users.new"))

    except:
        # flash("That name is already taken")
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
    pass
# edit users details


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
# funtion to update details
