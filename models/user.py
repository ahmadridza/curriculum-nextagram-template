from models.base_model import BaseModel
from werkzeug.security import check_password_hash, generate_password_hash
import peewee as pw
import re
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=False)
    password = pw.CharField(unique=True)

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
