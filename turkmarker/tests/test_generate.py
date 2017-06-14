#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Test the utilities functions"""

# Imports
import os
import unittest
from unittest import skip
from unittest.mock import patch, mock_open, Mock
import configparser
import numpy as np
from collections import OrderedDict
from turkmarker.utilities.base import parse_sys_config,\
    TEMPLATE_DATA, DEFAULT_SYS_CONFIG, DEFAULT_SAVE_FOLDER
from turkmarker.utilities.generate import GenerateSite,\
    CHECK_JS_INTRO, X_TEMPLATE, Y_TEMPLATE, JS_END

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Thursday 1 June  10:57:35 AEST 2017'
__license__ = 'BSD 3-Clause'


js_landmarks = np.array(
[
    [100, 200],
    [101, 402],
    [402, 603],
    [302, 603],
])

class MockConfigParser(configparser.ConfigParser):

    def __init__(self, *args, **kwargs):
        self._data = {
            'AWS-S3': {
                'BucketName': 'bucket',
                'Region': 'us-west-1',
                'ACL': 'public-read',
                },
            'AWS-MTURK' : {
                'EndPoint': 'http://www.mturk.com',
                'Region': 'us-west-1',
                'HIT_Title': 'title',
                'HIT_Description': 'desc',
                'HIT_Keywords': 'keywords',
                'HIT_Reward': '0.15',
                'HIT_Max_Assignments': '10',
                'HIT_LifetimeInSeconds': '20',
                'HIT_AssignmentDurationInSeconds': '2',
                'HIT_AutoApprovalDelayInSeconds': '1',
                'HIT_Frame_Height': '100',
                },
            'LANDMARK-DETAILS': {
                'Radius': '10',
                'BaseColour': '#ffffff',
                'HighlightColour': '#000000',
                'TemplateImage': 'template_face.png',
                'TemplateLandmarks': 'landmarks.csv',
                'StaticFolder': 'static_folder',
                'DisplayImage': 'display_image.png',
                'ResultsFolder': 'results_folder',
                'ConfigJSON': 'config_json.json',
                'CheckJS': 'check_js.js',
                }
        } 

    def read(self, *args, **kwargs):
        pass

    def __getitem__(self, key):
        return self._data[key]


class TestGenerateFiles(unittest.TestCase):


    def test_read_config(self):
        """Check config file read"""

        config = parse_sys_config(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                'testconfig')
        )
        self.assertEqual(config['AWS-S3']['BUCKET_NAME'], 'turklandmarker')
        self.assertEqual(config['AWS-S3']['REGION'], 'us-west-2')
        self.assertEqual(config['AWS-S3']['ACL'], 'public-read')
        self.assertEqual(config['AWS-MTURK']['END_POINT'], 'https://mturk-requester-sandbox.us-east-1.amazonaws.com')
        self.assertEqual(config['AWS-MTURK']['REGION'], 'us-east-1')
        self.assertEqual(config['AWS-MTURK']['HIT_TITLE'], 'Facial Landmarking')
        self.assertEqual(config['AWS-MTURK']['HIT_DESC'], 'Identify specified points on a face')
        self.assertEqual(config['AWS-MTURK']['HIT_REWARD'], '0.15')
        self.assertEqual(config['AWS-MTURK']['HIT_MAXASSIGN'], '10')
        self.assertEqual(config['AWS-MTURK']['HIT_LIFE'], '172800')
        self.assertEqual(config['AWS-MTURK']['HIT_ASSIGNDUR'], '600')
        self.assertEqual(config['AWS-MTURK']['HIT_AUTOAPPROVEDELAY'], '14400')
        self.assertEqual(config['AWS-MTURK']['HIT_FRAMEHEIGHT'], '800')
        self.assertEqual(config['KEYS']['AWS-ID'], '1234')
        self.assertEqual(config['KEYS']['AWS-KEY'], '456')

    @patch('os.path.exists', side_effect=[True])
    def test_default_override(self, exists_mock):
        """Test parse_sys_config returns non-default values"""

        with patch('configparser.ConfigParser', MockConfigParser) as m:
            config_no_defaults = parse_sys_config()

            # Check the no defaults
            self.assertEqual(config_no_defaults['LANDMARK-DETAILS']['TEMPLATE_IMAGE'],
                             m()['LANDMARK-DETAILS']['TemplateImage'])
            self.assertEqual(config_no_defaults['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS'],
                             m()['LANDMARK-DETAILS']['TemplateLandmarks'])
            self.assertEqual(config_no_defaults['LANDMARK-DETAILS']['STATIC_FOLDER'],
                             m()['LANDMARK-DETAILS']['StaticFolder'])
            self.assertEqual(config_no_defaults['LANDMARK-DETAILS']['DISPLAY_IMAGE'],
                             m()['LANDMARK-DETAILS']['DisplayImage'])
            self.assertEqual(config_no_defaults['LANDMARK-DETAILS']['RESULTS_FOLDER'],
                             m()['LANDMARK-DETAILS']['ResultsFolder'])
            self.assertEqual(config_no_defaults['LANDMARK-DETAILS']['CONFIG_JSON'],
                             m()['LANDMARK-DETAILS']['ConfigJSON'])
            self.assertEqual(config_no_defaults['LANDMARK-DETAILS']['CHECK_JS'],
                             m()['LANDMARK-DETAILS']['CheckJS'])


    def test_no_config(self):
        """Test assertion raises when config file doesn't exist"""

        with self.assertRaises(FileNotFoundError):
            config = parse_sys_config('no_config')
        

    @patch('numpy.genfromtxt', return_value=np.array([[1,2],[3,4]]))
    @patch('PIL.Image.Image.save')
    def test_correct_num_images_produces(self, mock_img, mock_pts):

        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_IMAGE': os.path.join(TEMPLATE_DATA, 'template_face.png'), 
                'TEMPLATE_LANDMARKS': os.path.join(TEMPLATE_DATA, 'template_landmarks.csv'), 
                'STATIC_FOLDER': DEFAULT_SAVE_FOLDER,
                'RADIUS': 3, 
                'BASE_COLOUR': '#FFFFFF', 
                'HI_COLOUR': '#FFFFFF', 
            }
        }

        GenerateSite(config).generate_lmrk_images()
        self.assertEqual(mock_img.call_count, 2)
        for i in range(2):
            mock_img.call_args_list[i].assert_called_with(
                os.path.join(DEFAULT_SAVE_FOLDER, 'lmrk_P%d.jpg' % i))

    @patch('numpy.genfromtxt', return_value=np.array([[1,2],[3,4]]))
    @patch('json.dump')
    @patch('builtins.open')
    def test_correct_json_points(self, mock_file, mock_json, mock_pts):
        """Test the config.json file is correctly generated"""

        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_LANDMARKS': os.path.join(TEMPLATE_DATA, 'template_landmarks.csv'), 
                'CONFIG_JSON': os.path.join(DEFAULT_SAVE_FOLDER, 'config.json'),
                }
            }

        GenerateSite(config).generate_config_json()

        # Test file open
        mock_file.assert_called_with(
            os.path.join(DEFAULT_SAVE_FOLDER, 'config.json'),
            'w')

        # Test json dump
        expected_results = OrderedDict()
        expected_results["P1"] = {"kind": "point"}
        expected_results["P2"] = {"kind": "point"}

        self.assertEqual(mock_json.call_count, 1)
        self.assertEqual(mock_json.call_args_list[0][0][0], expected_results)
        self.assertEqual(mock_json.call_args_list[0][1], {'indent': 4})

    @patch('numpy.genfromtxt', return_value=js_landmarks)
    def test_correct_javascript_rules(self, mock_pts):

        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_LANDMARKS': os.path.join(TEMPLATE_DATA, 'template_landmarks.csv'), 
                'CHECK_JS': os.path.join(DEFAULT_SAVE_FOLDER, 'check.js'),
                }
            }


        CHECK_JS = os.path.join(DEFAULT_SAVE_FOLDER, 'check.js')

        mock_file = mock_open()
        with patch('builtins.open', mock_file, create=True):
            GenerateSite(config).generate_javascript_check()
            self.assertEqual(mock_file.call_count, 2)
            mock_file.assert_any_call(CHECK_JS, 'w')
            mock_file.assert_called_with(CHECK_JS, 'a')

            # Check written contents
            handle = mock_file()
            handle.write.assert_any_call(CHECK_JS_INTRO)

            # Generate data string
            expected_results = ""
            expected_results += X_TEMPLATE.substitute(X1=3, X2=2)
            expected_results += X_TEMPLATE.substitute(X1=3, X2=4)
            expected_results += Y_TEMPLATE.substitute(X1=2, X2=1)
            expected_results += Y_TEMPLATE.substitute(X1=3, X2=2)
            expected_results += JS_END;

            handle.write.assert_any_call(expected_results)
