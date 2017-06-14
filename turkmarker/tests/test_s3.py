#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Test use of Mechanical Turk API"""

# Imports
import os
import unittest
import boto3
from unittest import skip
from unittest.mock import patch, MagicMock 
from turkmarker.aws.s3 import AWSS3, CONTENT_TYPES 


class TestS3API(unittest.TestCase):

    def setUp(self):
        self.config = {
            'AWS-S3': {
                'REGION': 'us-east-1',
                'BUCKET_NAME': 'bucket_name',
                'ACL': 'public-read',
                },
            'KEYS': {
                'AWS-ID': '123456',
                'AWS-KEY': '5678',
                },
            'LANDMARK-DETAILS': {
                'STATIC_FOLDER': 'static_folder',
                }
            }

        self.obj = AWSS3(self.config, debug_level=1)

    @patch('boto3.client', autospec=boto3.client)
    def test_connect(self, boto_mock):
        """Test connected Flag is set"""

        self.obj.connect()

        self.assertTrue(self.obj.connected)
        boto_mock.assert_called_with('s3',
            aws_access_key_id=self.config['KEYS']['AWS-ID'],
            aws_secret_access_key=self.config['KEYS']['AWS-KEY'],
            region_name=self.config['AWS-S3']['REGION'],
        )

    @patch('builtins.print')
    def test_generate_bucket_link(self, print_mock):
        """Test the bucket link generate by the class is correct"""

        link = self.obj.generate_bucket_link()

        expected_link = 'https://s3-us-east-1.amazonaws.com/bucket_name/index.html'

        self.assertEqual(link, expected_link)
        print_mock.assert_called_with(expected_link)

    @patch('boto3.client', autospec=boto3.client)
    def test_create_bucket_connected_no_exist(self, boto_mock):
        """Test creating a bucket on AWS - is connected - no existing buckets"""

        self.obj.connect()
        self.obj.s3.list_buckets = MagicMock(return_value={'Buckets': []})
        self.obj.s3.create_bucket = MagicMock()
        self.obj.create_bucket()

        self.obj.s3.create_bucket.assert_called_with(
            ACL=self.config['AWS-S3']['ACL'],
            Bucket=self.config['AWS-S3']['BUCKET_NAME'],
            CreateBucketConfiguration={
                 'LocationConstraint': self.config['AWS-S3']['REGION'],
                 }
            )

    @patch('boto3.client', autospec=boto3.client)
    def test_create_bucket_not_connected_no_exist(self, boto_mock):
        """Test creating a bucket on AWS - is not connected - no existing buckets"""

        self.obj.s3 = MagicMock()
        self.obj.s3.list_buckets = MagicMock(return_value={'Buckets': []})
        self.obj.s3.create_bucket = MagicMock()
        self.obj.create_bucket()

        self.obj.s3.create_bucket.assert_called_with(
            ACL=self.config['AWS-S3']['ACL'],
            Bucket=self.config['AWS-S3']['BUCKET_NAME'],
            CreateBucketConfiguration={
                 'LocationConstraint': self.config['AWS-S3']['REGION'],
                 }
            )

    @patch('builtins.print')
    def test_create_bucket_not_connected_bucket_exists(self, print_mock):
        """Test creating a bucket on AWS - is not connected - no existing buckets"""

        self.obj.connect = MagicMock()
        self.obj.s3 = MagicMock()
        self.obj.s3.list_buckets  = MagicMock(side_effect=lambda :{
            'Buckets': [{'Name':self.config['AWS-S3']['BUCKET_NAME']}]})
        bucket = self.obj.create_bucket()

        self.assertTrue(self.obj.connect.called)
        self.assertEqual(bucket, {'Name': 'bucket_name'})
        print_mock.assert_called_with('%s Bucket exists' %
            self.config['AWS-S3']['BUCKET_NAME'])

    @patch('builtins.print')
    @patch('boto3.client')
    def test_upload_file_connected(self, boto_mock, print_mock):
        """Test uploading files - is already connected"""

        example_files = [
            'test.html',
            'test.css',
            'test.jpg',
            'test.jpeg',
            'test.png',
            'test.svg',
            'test.js',
            'test.json',
            'test.eot',
            'test.woff',
            'test.ttf',
            'test.txt',
        ]

        def produce_files(*args, **kwargs):
            for filename in example_files:
                yield filename

        self.obj.connect()
        self.obj.s3.upload_file = MagicMock()

        with patch('os.listdir', side_effect=produce_files) as\
            listdir_mock:
        
            self.obj.upload_files()

            for filename in example_files:
                _, ext = os.path.splitext(filename)
                self.obj.s3.upload_file.assert_any_call(
                    os.path.join(self.config['LANDMARK-DETAILS']['STATIC_FOLDER'],
                        filename),
                    self.config['AWS-S3']['BUCKET_NAME'],
                    os.path.join(self.config['LANDMARK-DETAILS']['STATIC_FOLDER'],
                        filename),
                    ExtraArgs={
                        'ContentType': CONTENT_TYPES[ext],
                        'ACL': self.config['AWS-S3']['ACL'],
                    }
                )
                print_mock.assert_any_call(
                    'Uploading: %s' %
                    os.path.join(self.config['LANDMARK-DETAILS']['STATIC_FOLDER'],
                        filename)
                )

            for filename in ['index.html', 'error.html', 'protocol.html']:
                _, ext = os.path.splitext(filename)
                self.obj.s3.upload_file.assert_any_call(
                    filename,
                    self.config['AWS-S3']['BUCKET_NAME'],
                    filename,
                    ExtraArgs={
                        'ContentType': CONTENT_TYPES[ext],
                        'ACL': self.config['AWS-S3']['ACL'],
                    }
                )
                print_mock.assert_any_call(
                    'Uploading: %s' % filename)


    @patch('builtins.print')
    @patch('boto3.client')
    def test_upload_file_not_connected(self, boto_mock, print_mock):
        """Test the connect function is called if not otherwise connected""" 

        self.obj.connect = MagicMock()
        self.obj.s3 = MagicMock()
        self.obj.s3.upload_file = MagicMock()

        def produce_files(*args, **kwargs):
            for filename in ['test.css']:
                yield filename

        with patch('os.listdir', side_effect=produce_files) as\
            listdir_mock:
        
            self.obj.upload_files()

        self.assertTrue(self.obj.connect.called)
