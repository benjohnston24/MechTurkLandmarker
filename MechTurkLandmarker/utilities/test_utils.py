#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Test the utilities functions"""

# Imports
import os
import unittest
import numpy as nps
import pandas as pd
from collections import OrderedDict
from unittest.mock import MagicMock, patch
from utilities import generate_lmrk_images,\
    generate_config_json, SAVE_FOLDER,\
    CONFIG_JSON


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Thursday 1 June  10:57:35 AEST 2017'
__license__ = 'BSD 3-Clause'

class TestGenImages(unittest.TestCase):

    @patch('pandas.read_csv', return_value=pd.DataFrame([[1,2],[3,4]]))
    @patch('PIL.Image.Image.save')
    def test_correct_num_images_produces(self, mock_img, mock_pts):

        generate_lmrk_images()
        self.assertEqual(mock_img.call_count, 2)
        for i in range(2):
            mock_img.call_args_list[i].assert_called_with(
                os.path.join(SAVE_FOLDER, 'lmrk_P%d.jpg' % i))


class TestGenJSON(unittest.TestCase):

    @patch('pandas.read_csv', return_value=pd.DataFrame([[1,2],[3,4]]))
    @patch('json.dump')
    @patch('builtins.open')
    def test_correct_json_points(self, mock_file, mock_json, mock_pts):
        """Test the config.json file is correctly generated"""
        generate_config_json()

        # Test file open
        mock_file.assert_called_with(CONFIG_JSON, 'w')

        # Test json dump
        expected_results = OrderedDict()
        expected_results["P1"] = {"kind": "point"}
        expected_results["P2"] = {"kind": "point"}

        self.assertEqual(mock_json.call_count, 1)
        self.assertEqual(mock_json.call_args_list[0][0][0], expected_results)
        self.assertEqual(mock_json.call_args_list[0][1], {'indent': 4})
