from models.base_model import BaseModel
from models.image import Image
from models.user import User
import peewee as pw


class Donation(BaseModel):
    amount = pw.DecimalField(null=False)
    image = pw.ForeignKeyField(Image, backref="donations")
    user = pw.ForeignKeyField(User, backref="donations")
