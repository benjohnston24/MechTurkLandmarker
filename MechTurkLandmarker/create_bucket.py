import boto3
import os
import xmltodict

AWS_ACCESS_KEY_ID = os.getenv('MECHTURK_ID') 
AWS_SECRET_ACCESS_KEY = os.getenv('MECHTURK_KEY') 
BUCKET_NAME = 'turklandmarker4'
REGION_NAME = 'us-west-2' # Oregon

S3 = boto3.client('s3',
    region_name = REGION_NAME,
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
)

import pdb;pdb.set_trace()

if False:
    # Create Bucket
    response = S3.create_bucket(
        Bucket=BUCKET_NAME,
        ACL='public-read',
        CreateBucketConfiguration={
            'LocationConstraint': REGION_NAME,
        },
    )

    # Upload files
    file_list = [os.path.join('static', filename) for filename in os.listdir('static')]
    file_list.append('index.html')
    file_list.append('protocol.html')
    file_list.append('error.html')

file_list = ['index.html']

for upload_name in file_list:
    print(upload_name)
    S3.upload_file(upload_name, BUCKET_NAME, upload_name, ExtraArgs={'ContentType': 'text/html', 'ACL': 'public-read'}) 
    # Update permissions

import sys;sys.exit()
# Enable Website Configuration
# Create the configuration for the website
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

# Set the new policy on the selected bucket
S3.put_bucket_website(
    Bucket='my-bucket',
    WebsiteConfiguration=website_configuration
)
