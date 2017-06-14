#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Test use of Mechanical Turk API"""

# Imports
import os
import unittest
import boto3
import re
import numpy as np
from datetime import datetime, timedelta
from unittest import skip
from unittest.mock import MagicMock, patch,\
    mock_open
from turkmarker.aws.mturk import AWSMTurk,\
    EXTERNAL_Q_TEMPLATE


class TestMturkAPI(unittest.TestCase):

    def setUp(self):
        self.config = {
            'AWS-MTURK': {
                'REGION': 'us-east-1',
                'ACL': 'public-read',
                'END_POINT': 'https://www.mturk.com',
                'HIT_TITLE': 'HIT Title',
                'HIT_DESC': 'HIT Description',
                'HIT_KEYWORDS': 'keyword1, keyword2',
                'HIT_REWARD': '1.23',
                'HIT_MAXASSIGN': '2',
                'HIT_LIFE': '10',
                'HIT_ASSIGNDUR': '11',
                'HIT_AUTOAPPROVEDELAY': '12',
                'HIT_FRAMEHEIGHT': '600',
                },
            'KEYS': {
                'AWS-ID': '123456',
                'AWS-KEY': '5678',
                },
            'LANDMARK-DETAILS': {
                'RESULTS_FOLDER': 'results',
                },
            }

        self.hit_dict = {
            'HITs':[
                {'HITId': '1234',
                'Title': 'HIT 1',
                'Description': 'Desc 1'},
                {'HITId': '5678',
                'Title': 'HIT 2',
                'Description': 'Desc 2'},
                {'HITId': '9101112',
                'Title': 'HIT 3',
                'Description': 'Desc 3'},

                ]
            }


        self.question = EXTERNAL_Q_TEMPLATE.substitute(
            url='http://www.duckduckgo.com',
            frame_height=400)

        self.obj = AWSMTurk(self.config, debug_level=1)


    @patch('boto3.client', autospec=boto3.client)
    def test_connect(self, boto_mock):
        """Test connected Flag is set"""

        self.obj.connect()

        self.assertTrue(self.obj.connected)
        boto_mock.assert_called_with('mturk',
            aws_access_key_id=self.config['KEYS']['AWS-ID'],
            aws_secret_access_key=self.config['KEYS']['AWS-KEY'],
            region_name=self.config['AWS-MTURK']['REGION'],
            endpoint_url=self.config['AWS-MTURK']['END_POINT'],
        )

    @patch('boto3.client', autospec=boto3.client)
    def test_create_hit_connected(self, boto_mock):
        """Test creating a hit, where client is connected"""

        self.obj.connect()
        self.obj.mturk.create_hit = MagicMock()

        self.obj.create_HIT(self.question)

        self.obj.mturk.create_hit.assert_called_with(
            Title=self.config['AWS-MTURK']['HIT_TITLE'], 
            Description=self.config['AWS-MTURK']['HIT_DESC'], 
            Keywords=self.config['AWS-MTURK']['HIT_KEYWORDS'], 
            Reward=self.config['AWS-MTURK']['HIT_REWARD'], 
            MaxAssignments=int(self.config['AWS-MTURK']['HIT_MAXASSIGN']), 
            LifetimeInSeconds=int(self.config['AWS-MTURK']['HIT_LIFE']), 
            AssignmentDurationInSeconds=int(self.config['AWS-MTURK']['HIT_ASSIGNDUR']), 
            AutoApprovalDelayInSeconds=int(self.config['AWS-MTURK']['HIT_AUTOAPPROVEDELAY']), 
            Question=self.question,
            )

    @patch('boto3.client', autospec=boto3.client)
    def test_create_hit_not_connected(self, boto_mock):
        """Test creating a hit, where client is not connected"""

        self.obj.connect = MagicMock()
        self.obj.mturk = MagicMock()
        self.obj.mturk.create_hit = MagicMock()

        self.obj.create_HIT(self.question)

        self.assertEqual(self.obj.connect.call_count, 1)

        self.obj.mturk.create_hit.assert_called_with(
            Title=self.config['AWS-MTURK']['HIT_TITLE'], 
            Description=self.config['AWS-MTURK']['HIT_DESC'], 
            Keywords=self.config['AWS-MTURK']['HIT_KEYWORDS'], 
            Reward=self.config['AWS-MTURK']['HIT_REWARD'], 
            MaxAssignments=int(self.config['AWS-MTURK']['HIT_MAXASSIGN']), 
            LifetimeInSeconds=int(self.config['AWS-MTURK']['HIT_LIFE']), 
            AssignmentDurationInSeconds=int(self.config['AWS-MTURK']['HIT_ASSIGNDUR']), 
            AutoApprovalDelayInSeconds=int(self.config['AWS-MTURK']['HIT_AUTOAPPROVEDELAY']), 
            Question=self.question,
            )

    @patch('builtins.print')
    def test_create_external_question_XM(self, print_mock):
        """Test create an external hit"""

        url = 'http://stuff.com'
        result = self.obj.create_external_question_XML(url)

        self.assertEqual(EXTERNAL_Q_TEMPLATE.substitute(
            url=url,
            frame_height=self.config['AWS-MTURK']['HIT_FRAMEHEIGHT']),
            result)

        print_mock.assert_called_with(result)

    @patch('boto3.client')
    def test_list_hits_connected(self, boto_mock):
        """Test getting list of hits where client is connected"""

        self.obj.connect()
        self.obj.mturk.list_hits = MagicMock(side_effect=[self.hit_dict])

        result = self.obj.list_HITS()

        self.assertTrue(result,[
            ('1234', 'HIT 1', 'Desc 1'),
            ('5678', 'HIT 2', 'Desc 2'),
            ('9101112', 'HIT 3', 'Desc 3'),
            ])

    @patch('boto3.client')
    def test_list_hits_not_connected(self, boto_mock):
        """Test getting list of hits where client is not connected"""


        self.obj.connect = MagicMock()
        self.obj.mturk = MagicMock()
        self.obj.mturk.list_hits = MagicMock(side_effect=[self.hit_dict])

        result = self.obj.list_HITS()

        self.assertEqual(self.obj.connect.call_count, 1)

        self.assertTrue(result,[
            ('1234', 'HIT 1', 'Desc 1'),
            ('5678', 'HIT 2', 'Desc 2'),
            ('9101112', 'HIT 3', 'Desc 3'),
            ])

    @patch('boto3.client')
    def test_get_results_not_connected(self, boto_mock):
        """Test get results already not connected"""

        self.obj.connect = MagicMock()
        self.obj.mturk = MagicMock()

        self.obj.mturk.list_assignments_for_hit = MagicMock()
        self.obj.get_results('1234')

        self.assertEqual(self.obj.connect.call_count, 1)
        self.obj.mturk.list_assignments_for_hit.assert_called_with(
            HITId='1234',
            MaxResults=100,
            AssignmentStatuses=['Submitted','Approved', 'Rejected'])

    @patch('os.path.exists', side_effect=[False, False])
    @patch('os.mkdir')
    def test_manage_results_folder(self, mkdir_mock, exists_mock):
        """Test construction of the results folder"""

        hit_id = '1234'
        result = self.obj._manage_results_folder(hit_id)

        mkdir_mock.assert_any_call(
            self.config['LANDMARK-DETAILS']['RESULTS_FOLDER'])

        mkdir_mock.assert_any_call(
            os.path.join(
                self.config['LANDMARK-DETAILS']['RESULTS_FOLDER'],
                hit_id)
            )

        self.assertEqual(result,
            os.path.join(
                self.config['LANDMARK-DETAILS']['RESULTS_FOLDER'],
                hit_id)
            )


    @patch('os.path.exists', side_effect=[True, True])
    @patch('os.mkdir')
    def test_manage_results_folder_exists(self, mkdir_mock, exists_mock):
        """Test construction of the results folder where folders exist"""

        hit_id = '1234'
        self.obj._manage_results_folder(hit_id)
        self.assertEqual(mkdir_mock.call_count, 0)

    @patch('os.path.exists', side_effect=[True, True])
    def test_prepare_assignment_info_no_mkdir(self, exists_mock):
        """Test saving results to file"""

        results_folder = 'results_folder'
        self.obj._manage_results_folder = MagicMock(return_value=results_folder)

        # HIT Result
        create_time = datetime.now()
        accept_time = create_time + timedelta(3)
        accept_time2 = accept_time + timedelta(3)

        hit_id = '1234'
        hit_info = {
            'Title': 'HIT Title',
            'Description': 'HIT Desc',
            'CreationTime': create_time,
        }

        hit_result = {
            'NumResults': 2,
            'Assignments':[
                {
                    'WorkerId': '12345',
                    'AssignmentId': '6789',
                    'AcceptTime': accept_time,
                    'AssignmentStatus': 'Submitted',
                    'Answer': '',
                },
                {
                    'WorkerId': '67890',
                    'AssignmentId': '101112',
                    'AcceptTime': accept_time2,
                    'AssignmentStatus': 'Submitted',
                    'Answer': '',
                }

            ],
        }

        i = 0
        for result_dict, savename in self.obj._prepare_assignment_info(hit_id, hit_info, hit_result):
            with self.subTest(i=i):
                self.assertEqual(result_dict['Title'], hit_info['Title'])
                self.assertEqual(result_dict['Description'], hit_info['Description'])
                self.assertEqual(result_dict['CreationTime'], str(hit_info['CreationTime']))
                self.assertEqual(result_dict['WorkerId'], hit_result['Assignments'][i]['WorkerId'])
                self.assertEqual(result_dict['AssignmentId'], hit_result['Assignments'][i]['AssignmentId'])
                self.assertEqual(result_dict['AssignmentStatus'], hit_result['Assignments'][i]['AssignmentStatus'])
                self.assertEqual(result_dict['AcceptTime'], str(hit_result['Assignments'][i]['AcceptTime']))
                self.assertEqual(result_dict['Answers'], [])

                # Search the savename
                folder = os.path.join(results_folder, hit_result['Assignments'][i]['AssignmentId'])
                curr_folder = os.path.join(folder, r'\d{4}-\d{2}-\d{2}-\d{2}:\d{2}:\d{2}_\d{5}')
                pattern = re.compile(curr_folder)
                self.assertTrue(pattern.fullmatch(savename) is not None)
                i += 1

    @patch('os.mkdir')
    @patch('os.path.exists', side_effect=[False])
    def test_prepare_assignment_info_mkdir(self, exists_mock, mkdir_mock):
        """Test make directory is called"""

        results_folder = 'results_folder'
        self.obj._manage_results_folder = MagicMock(return_value=results_folder)

        # HIT Result
        create_time = datetime.now()
        accept_time = create_time + timedelta(3)
        accept_time2 = accept_time + timedelta(3)

        hit_id = '1234'
        hit_info = {
            'Title': 'HIT Title',
            'Description': 'HIT Desc',
            'CreationTime': create_time,
        }

        hit_result = {
            'NumResults': 2,
            'Assignments':[
                {
                    'WorkerId': '12345',
                    'AssignmentId': '6789',
                    'AcceptTime': accept_time,
                    'AssignmentStatus': 'Submitted',
                    'Answer': [],
                },

            ],
        }

        for result_dict, savename in self.obj._prepare_assignment_info(hit_id, hit_info, hit_result):
            pass
        self.assertEqual(mkdir_mock.call_count, 1)

    @patch('builtins.open')
    @patch('numpy.savetxt', autospec=np.savetxt)
    def test_save_results_to_file(self, savetxt_mock, file_mock):
        """Test saving the results to file"""

        self.obj.connect = MagicMock()
        self.obj.mturk = MagicMock()

        def func(*args, **kwargs):
            yield ({'Answers': [], 'Answer': []}, 'savename')

        self.obj._prepare_assignment_info = MagicMock(side_effect=func)

        xml_result = {
            'QuestionFormAnswers':{
                'Answer': [{
                    'QuestionIdentifier': 'marks',
                    'FreeText': "{\"P1\":[54,259],\"P2\":[55,291]}",
                }]
            }
        }

        with patch('xmltodict.parse', side_effect = [xml_result]) as xml_patch:
            self.obj.save_results_to_file('1234')

            self.assertEqual(savetxt_mock.call_count, 1)
            self.assertEqual(savetxt_mock.call_args[0][0], 'savename.csv')
            np.testing.assert_array_equal(
                    savetxt_mock.call_args[0][1],
                    np.array([[54, 259],[55, 291]]))
            self.assertEqual(savetxt_mock.call_args[1], {'delimiter': ','})

            file_mock.assert_any_call('savename.json', 'w')
