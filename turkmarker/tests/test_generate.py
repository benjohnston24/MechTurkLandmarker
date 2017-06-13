#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Test the utilities functions"""

# Imports
import os
import unittest
from unittest import skip
from unittest.mock import Mock, mock_open
import numpy as np
from collections import OrderedDict
from unittest.mock import MagicMock, patch
from turkmarker.utilities.base import parse_sys_config,\
    UTIL_FOLDER, DEFAULT_SYS_CONFIG, DEFAULT_SAVE_FOLDER
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


class TestGenerateFiles(unittest.TestCase):


    def test_default_config_exists(self):
        """Test the default config file exists"""

        self.assertTrue(os.path.exists(DEFAULT_SYS_CONFIG))

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

    @patch('numpy.genfromtxt', return_value=np.array([[1,2],[3,4]]))
    @patch('PIL.Image.Image.save')
    def test_correct_num_images_produces(self, mock_img, mock_pts):

        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_FACE': os.path.join(UTIL_FOLDER, 'template_face.png'), 
                'TEMPLATE_LANDMARKS': os.path.join(UTIL_FOLDER, 'template_landmarks.csv'), 
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
                'TEMPLATE_LANDMARKS': os.path.join(UTIL_FOLDER, 'template_landmarks.csv'), 
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
                'TEMPLATE_LANDMARKS': os.path.join(UTIL_FOLDER, 'template_landmarks.csv'), 
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