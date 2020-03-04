from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    filename = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref="images")

    @hybrid_property
    def has_filename(self):
        return f"https://nextagram-ridza.s3-ap-southeast-1.amazonaws.com/{self.filename}"

    @hybrid_property
    def total_donations(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            total = total + donation.amount
        return round(total)
