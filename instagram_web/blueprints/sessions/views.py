from flask import Blueprint, session, redirect, url_for, escape, request, flash, render_template
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import login_user, logout_user
from instagram_web.util.google_oauth import oauth


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder="templates")


@sessions_blueprint.route('/login', methods=['GET'])
def logindisplay():
    # display login form
    return render_template('sessions/new.html')


@sessions_blueprint.route('/login/new', methods=['POST'])
def login():
    # password keyed in by the user in the sign in form
    email_to_check = request.form.get('user_email')
    password_to_check = request.form.get('user_password')

    user = User.get_or_none(User.email == email_to_check)

    # password = User.get_or_none(User.password == password_to_check)
    hashed_password = user.password
    if not user:
        flash("Wrong email")
        return redirect(url_for("sessions.logindisplay"))

    # getting password from user which gets password from
    if not check_password_hash(hashed_password, password_to_check):
        flash("Wrong Password")
        return redirect(url_for("sessions.logindisplay"))
    else:
        login_user(user)
        flash("Your are now logged in")
        return redirect(url_for("users.index"))


@sessions_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out. Goodbye!")
    return redirect(url_for("sessions.logindisplay"))


@sessions_blueprint.route('/new')
def anything():
    pass


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/google_authorize")
def google_authorize():

    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

        user = User.get_or_none(User.email == email)

        if not user:
            flash('No user registered with this account')
            return redirect(url_for('sessions.new'))

    login_user(user)
    flash(f'Welcome back {user.name}')
    return redirect(url_for('users.edit', id=user.id))
