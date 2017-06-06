#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Script to manage AWS buckets to host the site"""

# Imports
import boto3
import os
import xmltodict
from utilities.base import parse_sys_config, UTIL_FOLDER,\
    DEFAULT_SYS_CONFIG

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 5 June  21:04:56 AEST 2017'
__license__ = 'MPL v2.0'


CONTENT_TYPES = {
    '.html': 'text/html',
    '.jpg' : 'image/jpg',
    '.jpeg': 'image/jpeg',
    '.png' : 'image/png',
    '.svg' : 'image/svg+xml',
    '.js'  : 'application/javascript',
    '.json': 'application/json',
    '.eot' : 'application/vnd.ms-fontobject',
    '.woff' : 'application/font-woff',
    '.ttf' : 'application/x-font-ttf',
}


class AWSS3(object):

    def __init__(self, config_file=DEFAULT_SYS_CONFIG, debug_level=1):
        """Constructor"""

        self.debug_level = debug_level
        self.config = parse_sys_config(config_file)

        self.s3 = boto3.client('s3',
            region_name=self.config['AWS-S3']['REGION'],
            aws_access_key_id=self.config['KEYS']['AWS-ID'],
            aws_secret_access_key=self.config['KEYS']['AWS-KEY'],
        )

        self.html_files = [
            'index.html',
            'protocol.html',
            'error.html',
            ]

    def create_bucket(self):
        """Create the bucket on AWS S3"""

        bucket_name = self.config['AWS-S3']['BUCKET_NAME']
        buckets = self.s3.list_buckets()['Buckets']

        exist_buckets = [bucket['Name'] for bucket in buckets]

        # The bucket already exists
        if bucket_name in exist_buckets:
            if self.debug_level:
                print("%s Bucket exists" % bucket_name)
            return buckets[exist_buckets.index(bucket_name)] 

        # Create the bucket
        return self.s3.create_bucket(
            ACL=self.config['AWS-S3']['ACL'],
            Bucket=bucket_name,
            CreateBucketConfiguration = {
                'LocationConstraint': self.config['AWS-S3']['REGION'],
            },
        )

    def upload_files(self):
        """Upload files to bucket""" 

        static_folder = self.config['LANDMARK-DETAILS']['STATIC_FOLDER']
        static_base = os.path.basename(static_folder)

        # Prepare the filenames and keys
        file_list = [
            (os.path.join(static_folder, filename), 
             os.path.join(static_base, os.path.basename(filename)))\
            for filename in os.listdir(static_folder)]

        # Add the files not included in the static folder
        file_list += [
            (filename, 
             os.path.basename(filename))\
            for filename in self.html_files]

        # Execute the upload
        for upload_name, upload_key in file_list:

            if self.debug_level:
                print("Uploading: %s" % upload_name)
            filename, ext = os.path.splitext(upload_name)
            self.s3.upload_file(
                upload_name,
                self.config['AWS-S3']['BUCKET_NAME'],
                upload_key,
                ExtraArgs={
                    'ContentType': CONTENT_TYPES[ext],
                    'ACL': 'public-read',
                },
            ) 


if __name__ == "__main__":
    s3 = AWSS3() 
    s3.create_bucket()
    s3.upload_files()
