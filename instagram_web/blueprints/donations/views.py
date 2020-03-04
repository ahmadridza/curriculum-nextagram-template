from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from models.image import Image
from models.donation import Donation
from instagram_web.util.braintree import gateway


donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash("No Image found with the Id selected")
        return redirect(url_for('users.index'))

    client_token = gateway.client_token.generate()

    if not client_token:
        flash("Unable to obtain token", "warning")
        return redirect(url_for('users.index'))

    return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/<image_id>/', methods=['POST'])
@login_required
def create(image_id):
    nonce = request.form.get('payment_method_nonce')

    if not nonce:
        flash('Invalid credit card details')
        return redirect(url_for('users.index'))

    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('No Image Found with provided id', 'warning')
        return redirect(url_for('users.index'))

    amount = request.form.get('amount')

    if not amount:
        flash('No donation amount provided', 'warning')
        return redirect(url_for('users.index'))

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if not result.is_success:
        flash('Unable to complete transaction', 'warning')
        return redirect(request.referrer)

    donation = Donation(amount=amount, image_id=image.id,
                        user_id=current_user.id)

    if not donation.save():
        flash('Donation successful but error creating record', 'warning')
        return redirect(url_for('users.index'))

    flash(f'Successfully donated RM{amount}', 'success')
    return redirect(url_for('users.index'))
