#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Class to submit and monitor mechanical turk task"""

# Imports
import boto3
import os
import xmltodict
import json
import pandas as pd
from collections import OrderedDict
from ast import literal_eval
from string import Template
from datetime import datetime
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

class AWSMTurk(object):

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

    def create_external_question_XML(self, url):
        """Construct the xml string for an external HIT question

        Parameters:
        url: the https url hosting the external question

        frame_height: the height of the external page in the HIT frame
        """

        self.external_question = EXTERNAL_Q_TEMPLATE.substitute(
            url=url, frame_height=self.config['AWS-MTURK']['HIT_FRAMEHEIGHT'])
        
        if self.debug_level:
            print(self.external_question)

        return self.external_question 

    def list_HITS(self):
        """List the currently submitted HITS"""

        if not self.connected:
            self.connect()

        hits = self.mturk.list_hits()
        hit_summary = []

        for hit in hits['HITs']:
            hit_summary.append((
                hit['HITId'],
                hit['Title'],
                hit['Description'],
                )
            )
        return hit_summary

    def get_results(self, hit_id, 
        status=['Submitted', 'Approved', 'Rejected']):
        """Get the results for a particular HIT""" 

        if not self.connected:
            self.connect()

        results = self.mturk.list_assignments_for_hit(
            HITId=hit_id,
            AssignmentStatuses=status)

        return results

    def save_results_to_file(self, hit_id,
        status=['Submitted', 'Approved', 'Rejected']):
        """Save the results to a file"""

        results_folder = self.config['LANDMARK-DETAILS']['RESULTS_FOLDER']
        # If the folder doesnt exist, make it
        if not os.path.exists(results_folder):
            os.mkdir(results_folder)

        # Create a HIT specific folder in the results folder
        hit_results_folder = os.path.join(results_folder, hit_id)
        if not os.path.exists(hit_results_folder):
            os.mkdir(hit_results_folder)

        hit_results = self.get_results(hit_id, status)

        results = []
        marks = None
        for hit_result in hit_results['Assignments']:
            savename = "{}_{}".format(
                    datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                    hit_result['WorkerId'])
            savename = os.path.join(hit_results_folder, savename)
            result_dict = {}
            result_dict['WorkerId'] = hit_result['WorkerId']
            result_dict['AssignmentId'] = hit_result['AssignmentId']
            result_dict['AssignmentStatus'] = hit_result['AssignmentStatus']
            result_dict['AcceptTime'] = str(hit_result['AcceptTime'])
            result_dict['Answers'] = []

            # Parse Answer into
            xml_dict = xmltodict.parse(hit_result['Answer'])
            # There are multiple fields in the HIT layout
            for field in xml_dict['QuestionFormAnswers']['Answer']:
                result_dict['Answers'].append(field)
                if 'marks' in field['QuestionIdentifier']:
                    marks = field['FreeText']
                    marks = literal_eval(marks)
                    organised_marks = OrderedDict()
                    for i in range(1, len(marks.keys()) + 1):
                        organised_marks['P%d' % i] = marks['P%d' % i]
                    df = pd.DataFrame(organised_marks)
                    df = pd.DataFrame(df.values.T)
                    df.to_csv("%s.csv" % savename, index=False)

            with open("%s.json" % savename, 'w') as f:
                f.write(json.dumps(result_dict))
                #json.dump(f, result_dict)



            # Dump the result dict 


if __name__ == "__main__":
    mturk = AWSMTurk()
    hits = mturk.list_HITS()
    import pdb;pdb.set_trace()
    #mturk.save_results_to_file('3WRBLBQ2GRQ18817I3SW57AVWZ2G0I')
    #import sys;sys.exit()
    #results = mturk.get_results(hits[2][0])
    #import pdb;pdb.set_trace()
    #import xmltodict
    #results = xmltodict.parse(results['Assignments'][0]['Answer'])
    #import json
    #with open('results.json', 'w') as f:
    #    f.write(json.dumps(results))
    #print(mturk.get_results(hits[2][0]))
#    print(mturk.list_HITS())
    #print(mturk.get_balance())
    #ext_question = mturk.create_external_question_XML('https://s3-us-west-2.amazonaws.com/turklandmarker/index.html', 800)
    #print(mturk.create_HIT(ext_question))
