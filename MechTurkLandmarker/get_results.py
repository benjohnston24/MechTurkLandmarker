#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
import boto3
import os
import xmltodict


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Friday 2 June  13:21:42 AEST 2017'
__license__ = 'BSD-3 Clause'

region_name = 'us-east-1'
aws_access_key_id = os.getenv('MECHTURK_ID') 
aws_secret_access_key = os.getenv('MECHTURK_KEY') 

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# Uncomment this line to use in production
# endpoint_url = 'https://m3QE4DGPGBRTI7WJ814FYHA08DAM4GOturk-requester.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
    endpoint_url = endpoint_url,
    region_name = region_name,
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key,
)
# Use the hit_id previously created
hit_id = "3QE4DGPGBRTI7WJ814FYHA08DAM4GO"

# We are only publishing this task to one Worker
# So we will get back an array with one item if it has been completed

worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted'])

if worker_results['NumResults'] > 0:
   for assignment in worker_results['Assignments']:
      xml_doc = xmltodict.parse(assignment['Answer'])
      
      print("Worker's answer was:")
      if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
         # Multiple fields in HIT layout
         for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
            print("For input field: " + answer_field['QuestionIdentifier'])
            print("Submitted answer: " + answer_field['FreeText'])
      else:
         # One field found in HIT layout
         print("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
         print("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
else:
   print("No results ready yet")
