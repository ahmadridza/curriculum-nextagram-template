from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Image(BaseModel):
    filename = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref="images")
