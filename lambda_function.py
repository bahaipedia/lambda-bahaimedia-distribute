import urllib
import boto3
import ast
import json
print('Loading function')

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sns_message = ast.literal_eval(event['Records'][0]['Sns']['Message'])
    target_bucket = context.function_name
    source_bucket = str(sns_message['Records'][0]['s3']['bucket']['name'])
    key = str(urllib.parse.unquote_plus(sns_message['Records'][0]['s3']['object']['key']))
    copy_source = {'Bucket': source_bucket, 'Key': key}
    print(f"Copying {key} from bucket {source_bucket} to bucket {target_bucket}...")
    try:
        s3.copy_object(Bucket=target_bucket, Key=key, CopySource=copy_source)
    except Exception as e:
        print(f'[Error] Copying {key} failed: {e}')
    else:
        print(f'[OK] Copied the {key} key successfully')
