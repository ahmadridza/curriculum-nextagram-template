import boto3
import botocore
from config import Config

ALLOWED_EXTENSIONS = set(['pdf', 'jpg', 'png', 'jpeg', 'gif'])

s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.S3_KEY,
    aws_secret_access_key=Config.S3_SECRET
)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_files_to_s3(file, bucket_name):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )

        return True

    except Exception as e:

        return False
