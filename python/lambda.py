import StringIO
import zipfile
import mimetypes
import json
import boto3
from botocore.client import Config

def lambda_handler(event, context):
    location = {
        "bucketName": 'build.fizzbuzzbang.com',
        "objectKey": 'build-fizzbuzzbang.zip'
    }
    job = event.get("CodePipeline.job")
    if job:
        for artifact in job["data"]["inputArtifacts"]:
            if artifact["name"] == "buildFizzbuzzbang":
                location = artifact["location"]["s3Location"]

    print("Building from " + str(location))

    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

    build_bucket = s3.Bucket(location["bucketName"])
    static_bucket = s3.Bucket('fizzbuzzbang.com')
    codebuild_zip = StringIO.StringIO()
    build_bucket.download_fileobj(location["objectKey"], codebuild_zip)

    with zipfile.ZipFile(codebuild_zip) as zips:
        for filename in zips.namelist():
            obj = zips.open(filename)
            static_bucket.upload_fileobj(obj, filename, ExtraArgs={'ContentType': mimetypes.guess_type(filename)[0]})
            static_bucket.Object(filename).Acl().put(ACL='public-read')
    if job:
        codepipeline = boto3.client('codepipeline')
        codepipeline.put_job_success_result(jobId=job["id"])
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda completed successfully')
    }
