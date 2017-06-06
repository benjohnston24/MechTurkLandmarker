#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Class to submit and monitor mechanical turk task"""

# Imports
import boto3
import os
import xmltodict
from string import Template
from utilities.base import parse_sys_config, UTIL_FOLDER,\
    DEFAULT_SYS_CONFIG

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Tuesday 6 June  16:29:28 AEST 2017'
__license__ = 'MPL v2.0'

EXTERNAL_Q_TEMPLATE = Template(
"""<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
      <ExternalURL>$url</ExternalURL>
      <FrameHeight>$frame_height</FrameHeight>
</ExternalQuestion>
""")

class AWSMturk(object):

    def __init__(self, config_file=DEFAULT_SYS_CONFIG, debug_level=1):
        """Constructor"""

        self.debug_level = debug_level
        self.config = parse_sys_config(config_file)
        self.connected = False

    def connect(self):
        """Connect""" 
        self.mturk = boto3.client('mturk',
            endpoint_url=self.config['AWS-MTURK']['END_POINT'],
            region_name=self.config['AWS-MTURK']['REGION'],
            aws_access_key_id=self.config['KEYS']['AWS-ID'],
            aws_secret_access_key=self.config['KEYS']['AWS-KEY'],
        )
        self.connected = True

    def get_balance(self):
        """Print the mechanical turk balance"""

        if not self.connected:
            self.connect()

        return self.mturk.get_account_balance()['AvailableBalance']

    def create_HIT(self, question):
        """Create a HIT

        Parameters:
        question: The XML text of the question for the HIT as a string
        """

        if not self.connected:
            self.connect()

        new_hit = self.mturk.create_hit(
            Title=self.config['AWS-MTURK']['HIT_TITLE'],
            Description=self.config['AWS-MTURK']['HIT_DESC'],
            Keywords=self.config['AWS-MTURK']['HIT_KEYWORDS'],
            Reward=self.config['AWS-MTURK']['HIT_REWARD'],
            MaxAssignments=int(self.config['AWS-MTURK']['HIT_MAXASSIGN']),
            LifetimeInSeconds=int(self.config['AWS-MTURK']['HIT_LIFE']),
            AssignmentDurationInSeconds=int(self.config['AWS-MTURK']['HIT_ASSIGNDUR']),
            AutoApprovalDelayInSeconds=int(self.config['AWS-MTURK']['HIT_AUTOAPPROVEDELAY']),
            Question=question,
        )

        return new_hit

    def create_external_question_XML(self, url, frame_height):
        """Construct the xml string for an external HIT question

        Parameters:
        url: the https url hosting the external question

        frame_height: the height of the external page in the HIT frame
        """

        self.external_question = EXTERNAL_Q_TEMPLATE.substitute(
            url=url, frame_height=frame_height)

        return self.external_question 

if __name__ == "__main__":
    mturk = AWSMturk()
    print(mturk.get_balance())
    ext_question = mturk.create_external_question_XML('https://s3-us-west-2.amazonaws.com/turklandmarker/index.html', 800)
    print(mturk.create_HIT(ext_question))
