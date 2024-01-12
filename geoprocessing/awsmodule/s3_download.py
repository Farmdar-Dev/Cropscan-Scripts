import boto3
from botocore.exceptions import ClientError
from boto3 import client
import os

def download_shp_file(bucket, output_path, shps, access_key, secret_key):

    session = boto3.session.Session(aws_access_key_id = access_key,
                                        aws_secret_access_key = secret_key)
    s3_client = session.client('s3')
    prefixes = shps.split(',')
    shp_paths = []
    folder_name = os.path.split(prefixes[0].split('.')[0].split(f"{bucket}/")[-1])[-1]
    final_folder_path = os.path.join(output_path, folder_name)
    if not os.path.exists(final_folder_path):
        os.makedirs(final_folder_path)
    for i in prefixes:
        pre = i.split('.')[0].split(f"{bucket}/")[-1]
        folder_name = os.path.split(pre)[-1]
        final_folder_path = os.path.join(output_path, folder_name)
        if not os.path.exists(final_folder_path):
            os.makedirs(final_folder_path)
        response = s3_client.list_objects_v2(
                        Bucket=bucket,
                        Prefix=f"{pre}.")
        print(f"{pre}.")
        files2down = []
        for content in response.get('Contents', []):
            file_name = content['Key'].replace(pre, '').split('.')
            if len(file_name) == 2:
                if not '/' in file_name[0] and file_name[1]:
                    files2down.append(content['Key'])
        shp_path = None
        for i in files2down:
            file = os.path.split(i)[-1]
            file_path = os.path.join(final_folder_path, file)
            s3_client.download_file(bucket, i, file_path)
            if file_path.endswith(".shp"):
                shp_path = file_path
                shp_paths.append(shp_path)
    return shp_paths

def download_boundaries(bucket, output_path, aoi_dict, access_key, secret_key):
    session = boto3.session.Session(aws_access_key_id = access_key,
                                        aws_secret_access_key = secret_key)
    s3_client = session.client('s3')
    boundaries = {}
    boundary_file_name = aoi_dict[list(aoi_dict.keys())[0]].split(f"{bucket}/")[-1].split('.')[0]
    folder_name = os.path.split(boundary_file_name)[-1]
    final_folder_path = os.path.join(output_path, folder_name)
    if not os.path.exists(final_folder_path):
        os.makedirs(final_folder_path)
    for key in aoi_dict:
        pre = aoi_dict[key].split(f"{bucket}/")[-1].split('.')[0]
        response = s3_client.list_objects_v2(
                        Bucket=bucket,
                        Prefix=pre)
        files2down = []
        for content in response.get('Contents', []):
            file_name = content['Key'].replace(pre, '').split('.')
            if len(file_name) == 2:
                if not '/' in file_name[0] and file_name[1]:
                    files2down.append(content['Key'])

        for i in files2down:
            file = os.path.split(i)[-1]
            file_path = os.path.join(final_folder_path, file)
            s3_client.download_file(bucket, i, file_path)
        boundaries[key] = file_path
    return boundaries

def download_esurvey(bucket, output_path, esurvey_s3, access_key, secret_key):
    session = boto3.session.Session(aws_access_key_id = access_key,
                                        aws_secret_access_key = secret_key)
    s3_client = session.client('s3')
    file = os.path.split(esurvey_s3)[-1]
    file_path = os.path.join(output_path, file)

    s3_client.download_file(bucket, esurvey_s3.split(f"{bucket}/")[-1], file_path)

    return file_path

