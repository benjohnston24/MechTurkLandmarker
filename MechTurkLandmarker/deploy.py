#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Python script to deploy site to AWS S3 and Mechanical Turk"""

# Imports
import argparse
from utilities.base import DEFAULT_SYS_CONFIG
from utilities.aws_s3 import AWSS3 
from utilities.aws_mturk import AWSMTurk

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Wednesday 7 June  13:52:10 AEST 2017'
__license__ = 'MPL v2.0'


def get_options(argv=None):

    parser = argparse.ArgumentParser(
        description="Build and Deploy to AWS S3 and Mechanical Turk",
        epilog="See https://github.com/benjohnston24/MechTurkLandmarker"
        " for more information")

    parser.add_argument('-u', '--upload', dest='upload', action='store_true',
        help='Upload files to S3', required=False)
    parser.add_argument('-m', '--mturk', dest='mturk', action='store_true',
        help='Create mechanical turk task', required=False)
    parser.add_argument('-c', '--config', type=str, dest='config_file',
        default=DEFAULT_SYS_CONFIG,
        help='Specify configuration file', required=False)
    parser.add_argument('-d', '--debug', dest='debug_level', type=int,
        help='Debug level 0: No debugging, 1: sys.stdout debugging', required=False, default=0)

    return parser.parse_args()

def _main(args=None):

    args = get_options(args)

    s3 = AWSS3(config_file=args.config_file,
               debug_level=args.debug_level)
    if args.upload:
        s3.create_bucket()
        s3.upload_files()

    if args.mturk:
        mturk = AWSMTurk(config_file=args.config_file,
            debug_level=args.debug_level)
        ext_question = mturk.create_external_question_XML(
            s3.generate_bucket_link())
        mturk.create_HIT(ext_question)

if __name__ == "__main__":
    _main()
