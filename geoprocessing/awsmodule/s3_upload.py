import boto3
from botocore.exceptions import ClientError
from boto3 import client
import os
from dotenv import load_dotenv

def upload_files(s3_path, local_file_path, folder_str):
    load_dotenv()
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket_name = bucket = os.getenv("bucket")
    session = boto3.session.Session(aws_access_key_id = aws_access_key_id,
                                                 aws_secret_access_key = aws_secret_access_key)
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)

    key = s3_path.split(f"{bucket_name}/")[-1]

    file_name = os.path.split(local_file_path)[-1]
    final_s3_path = f"{key}{folder_str}/{file_name}"
    print(f"Uploading {folder_str}...")
    bucket.upload_file(local_file_path, final_s3_path)
    return final_s3_path
    