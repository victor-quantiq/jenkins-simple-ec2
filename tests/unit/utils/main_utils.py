import os
import json
import logging
from zipfile import ZipFile

import boto3

AWS_REGION = 'eu-west-3'
AWS_PROFILE = 'localstack'
# ENDPOINT_URL = os.environ.get('LOCALSTACK_ENDPOINT_URL')
ENDPOINT_URL='http://localhost:4566'
LAMBDA_ZIP = './function.zip'

boto3.setup_default_session(profile_name=AWS_PROFILE)

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

def get_boto3_client(service):
    try:
        logger.info("endpoint url: " + str(ENDPOINT_URL))
        lambda_client = boto3.client (
            service,
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connectiong to LocalStack')
        raise e
    else:
        return lambda_client


def create_lambda_zip(function_path):

    logger.info("endpoint url: " + str(ENDPOINT_URL))
    try:
        with ZipFile(LAMBDA_ZIP, 'w') as zip:
            os.chdir('hello_world')
            zip.write('app.py')
            os.chdir('../')
    except Exception as e:
        logger.exception('Error while creating ZIP file.')
        raise e

def create_lambda(function_path, function_name):

    try:
        lambda_client=get_boto3_client('lambda')
        _=create_lambda_zip(function_path)
        
        with open(LAMBDA_ZIP, 'rb') as f:
            zipped_code = f.read()
            logger.info('zipped code: ' + str(zipped_code))

        lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.8',
            Role='role',
            Handler=function_name+ '.lambda_handler',
            Code=dict(ZipFile=zipped_code)
        )
    except Exception as e:
        logger.exception('Error while creating function')
        raise e

def invoke_function(function_name):

    try:
        lambda_client = get_boto3_client('lambda')
        response = lambda_client.invoke(
            FunctionName=function_name
        )
        return json.loads(
            response['Payload']
            .read()
            .decode('utf-8')
        )
    except Exception as e:
            logger.exception('Error while invoking function')
            raise e