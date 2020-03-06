import peeweedbevolve
from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for
from models.user import User
from models.image import Image
from flask_login import current_user, login_required, login_user
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_files_to_s3
from config import Config

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
@login_required
def show(username):

    user = User.get_or_none(User.name == username)

    if not user:
        flash(f'No User With that Usernam {username}')
        return redirect(url_for('users.index'))

    return render_template('users/show.html', user=user)

# reder template for
# display single user


@users_blueprint.route('/index', methods=['GET'])
def index():
    images = Image.select().where(Image.user_id != current_user.id)
    return render_template('users/index.html', images=images)
# display all users


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    if not str(current_user.id) == id:
        flash(f"You are not authorized to update this page")
        return redirect(url_for('users.edit', id=current_user.id))

    user = User.get_or_none(User.id == id)

    if current_user:
        if not user:
            flash(f"You're in the wrong neighborhood boy")
            return redirect(url_for("home"))
        else:
            return render_template("users/edit.html", user=user)


@users_blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    if not 'user_file' in request.files:
        flash('No image has been provided')
        return redirect(url_for('users.edit', id=current_user.id))

    file = request.files.get('user_file')

    file.filename = secure_filename(file.filename)

# how is the S3 triggering?
    if not upload_files_to_s3(file, Config.S3_BUCKET):
        flash("Oops something went wrong when uploading")
        return redirect(url_for('users.edit', id=current_user.id))

    update = User.update(profile_image=file.filename).where(
        User.id == current_user.id)

    update.execute()

    flash("Image upload Sucess!")
    return redirect(url_for('users.edit', id=current_user.id))
