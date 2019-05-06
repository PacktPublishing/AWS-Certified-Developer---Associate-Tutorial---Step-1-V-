import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.CRITICAL)

def connect_to_s3_resource(region_name):
    try:
        return boto3.resource('s3', region_name=region_name)
    except Exception:
        logger.error('Error connecting to S3 resource for region {}!'.format(region_name))
        raise Exception('HTTP500')

def connect_to_s3_client(region_name):
    try:
        return boto3.client('s3', region_name=region_name)
    except Exception:
        logger.error('Error connecting to S3 client for region {}!'.format(region_name))
        raise Exception('HTTP500')

def upload_to_bucket(fname, local_path, s3, bucket, ExtraArgs):
    s3.Object(bucket, fname).upload_fileobj(local_path, ExtraArgs=ExtraArgs)
    logger.info('Uploaded file {}'.format(fname))

def retrieve_objects_from_s3(s3_client,bucket):
    all_objects = s3_client.list_objects_v2(Bucket=bucket).get('Contents')
    if all_objects:
        return [(obj.get('Key'),s3_object_meta(s3_client,bucket,obj.get('Key'))) for obj in all_objects]
    return []

def s3_object_meta(s3_client, bucket, file_name):
    try:
        meta = s3_client.head_object(Bucket=bucket, Key=file_name)
        return meta.get('Metadata')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return None
        else:
            logger.exception('Unexpected exception while querying s3 bucket {} for file {}'.format(bucket, file_name))
            raise Exception('HTTP500')
