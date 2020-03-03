from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
from instagram_web.util.helpers import upload_files_to_s3
from config import Config


images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/myprofile', methods=['GET'])
def new():
    images = Image.select()
    user = current_user
    return render_template('images/myprofile.html', images=images, user=user)


@images_blueprint.route('/myprofile/new', methods=['POST'])
@login_required
def upload():

    if 'user_file' not in request.files:
        flash('No image has been provided')
        return redirect(url_for('images.new'))

    file = request.files.get('user_file')

    file.filename = secure_filename(file.filename)

    if not upload_files_to_s3(file, Config.S3_BUCKET):
        flash("Oops something went wrong when uploading")
        return redirect(url_for('images.new', id=current_user.id))

    display = Image(user=current_user.id, filename=file.filename)

    display.save()

    flash("Image upload Sucess!")
    return redirect(url_for('images.new', id=current_user.id))
