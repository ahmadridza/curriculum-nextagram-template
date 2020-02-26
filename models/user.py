from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=False)
    password = pw.CharField(unique=True)

# do the validation here

# def validate(self, )
#     if email(unique= True)
#         email = email
#         else:
#             "Please "
