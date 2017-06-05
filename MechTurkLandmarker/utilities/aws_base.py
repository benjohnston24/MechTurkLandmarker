#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Common AWS API components"""

# Imports
import configparser
import os
from string import Template

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 5 June  21:04:56 AEST 2017'
__license__ = 'MPL v2.0'

AWS_ACCESS_KEY_ID = os.getenv('MECHTURK_ID') 
AWS_SECRET_ACCESS_KEY = os.getenv('MECHTURK_KEY') 

EXTERNAL_Q_TEMPLATE = Template(
"""<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
      <ExternalURL>$url</ExternalURL>
      <FrameHeight>$frame_height</FrameHeight>
</ExternalQuestion>
""")

DEFAULT_SYS_CONFIG = os.path.join(
    os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_SYS_CONFIG = os.path.join(DEFAULT_SYS_CONFIG, '.configrc')


def parse_sys_config(config_file=DEFAULT_SYS_CONFIG):
    """Parse the config file
    
    Parameters:
    config_file: The path of the config file to read
    If is None, .configrc in the base directory is used
    
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    # Extract the info
    data =  {
        'AWS-S3': 
        {
            'BUCKET_NAME': config['AWS-S3']['BucketName'],
            'REGION': config['AWS-S3']['Region'],
            'ACL': config['AWS-S3']['ACL'], 
        },
        'AWS-MTURK':
        {
            'END_POINT': config['AWS-MTURK']['EndPoint'],
            'REGION': config['AWS-MTURK']['Region'],
            'HIT_TITLE': config['AWS-MTURK']['HIT_Title'],
            'HIT_DESC': config['AWS-MTURK']['HIT_Description'],
            'HIT_REWARD': config['AWS-MTURK']['HIT_Reward'],
            'HIT_MAXASSIGN': config['AWS-MTURK']['HIT_Max_Assignments'],
            'HIT_LIFE': config['AWS-MTURK']['HIT_LifetimeInSeconds'],
            'HIT_ASSIGNDUR': config['AWS-MTURK']['HIT_AssignmentDurationInSeconds'],
            'HIT_AUTOAPPROVEDELAY': config['AWS-MTURK']['HIT_AutoApprovalDelayInSeconds'],
            'HIT_FRAMEHEIGHT': config['AWS-MTURK']['HIT_Frame_Height'],
        }
    }
    return data
