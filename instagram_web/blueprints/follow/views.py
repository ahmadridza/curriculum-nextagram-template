from flask import Blueprint, redirect, url_for, render_template, request, flash
from models.user import User
from models.follower_following import FollowerFollowing
from flask_login import current_user, login_required


follows_blueprint = Blueprint("follows", __name__, template_folder="templates")


@follows_blueprint.route("/<idol_id>", methods=["POST"])
@login_required
def create(idol_id):

    idol = User.get_or_none(User.id == idol_id)

    if not idol:
        flash('No user found with this ID')
        return redirect(url_for('users.index'))

    new_follow = FollowerFollowing(
        fan_id=current_user.id,
        idol_id=idol.id
    )

    if not new_follow.save():
        flash('Unable to follow this user!')
        return redirect(url_for('users.show', username=idol.name))

    else:
        flash(f'You are now following{idol.name}')
        return redirect(url_for('users.show', username=idol.name))

    flash('Follow request sent! Please wait for approval')
    return redirect(url_for('users.show', username=idol.name))


@follows_blueprint.route("/<idol_id>/delete", methods=["POST"])
def delete(idol_id):

    follow = FollowerFollowing.get_or_none((FollowerFollowing.idol_id == idol_id) and (
        FollowerFollowing.fan_id == current_user.id))
    if follow.delete_instances():
        flash(f'You have unfollowed {follow.idol.name}')
        return redirect(url_for('users.show', username=follow.idol.name))
