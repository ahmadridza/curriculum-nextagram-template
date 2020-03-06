from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")
    idol = pw.ForeignKeyField(User, backref="fans")

    class Meta:
        indexes = ((('fan', 'idol'), True),)
