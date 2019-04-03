import StringIO
import zipfile
import mimetypes
import json
import boto3
from botocore.client import Config

def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

    build_bucket = s3.Bucket('build.fizzbuzzbang.com')
    static_bucket = s3.Bucket('fizzbuzzbang.com')
    codebuild_zip = StringIO.StringIO()
    build_bucket.download_fileobj('build-fizzbuzzbang.zip', codebuild_zip)

    with zipfile.ZipFile(codebuild_zip) as zips:
        for filename in zips.namelist():
            obj = zips.open(filename)
            static_bucket.upload_fileobj(obj, filename, ExtraArgs={'ContentType': mimetypes.guess_type(filename)[0]})
            static_bucket.Object(filename).Acl().put(ACL='public-read')

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda completed successfully')
    }
