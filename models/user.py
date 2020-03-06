from models.base_model import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash
import peewee as pw
import re
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property, hybrid_method


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=False)
    password = pw.CharField(unique=True)
    profile_image = pw.CharField(null=True)

    def validate(self):
        if len(self.password) < 6:  # if password length is less than six (self.password is from the class User which we specify in views.py templates/user/blueprint)
            # append this message to the error page
            self.errors.append('Password has to be longer than 6 characters.')
        # re.search to find r"\d find a digit or numbers in a string in self.password)
        if not re.search(r"\d", self.password):
            self.errors.append('Password must contain at least one digit')
        if not any(char.isupper() for char in self.password):
            self.errors.append(
                'Password requires at least an Upper Case Letter.')
        if not any(char.islower() for char in self.password):
            self.errors.append(
                'Password requires at least an Lower Case Letter'
            )
        else:
            self.password = generate_password_hash(self.password)
        if User.get_or_none(User.email == self.email):
            self.errors.append("Email is not unique")

    @hybrid_property
    def has_profile_image(self):
        return f"https://nextagram-ridza.s3-ap-southeast-1.amazonaws.com/{self.profile_image}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @hybrid_method
    def is_following(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none(
            (FollowerFollowing.fan_id == user.id) &
            (FollowerFollowing.idol_id == self.id)
        ) else False

    @hybrid_method
    def is_followed_by(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none(
            (FollowerFollowing.fan_id == self.id) &
            (FollowerFollowing.idol_id == user.id)
        ) else False
