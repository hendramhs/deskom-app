import boto3
from config import Config

def upload_file(file):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION
    )

    filename = file.filename

    s3.upload_fileobj(
        file,
        Config.AWS_BUCKET_NAME,
        filename
    )

    url = f"https://{Config.AWS_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return url