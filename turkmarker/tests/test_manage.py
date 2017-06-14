#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
import unittest
from unittest import skip
from unittest.mock import patch, MagicMock 
from turkmarker.manage import _main, get_options
from turkmarker.utilities.base import TEMPLATE_DATA

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Wednesday 14 June  16:33:58 AEST 2017'
__license__ = 'MPL v2.0'


class TestArgs(unittest.TestCase):
    
    def test_new_project(self):
        """Test options to construct new project"""
        options = get_options(['-n', 'new_project'])
        self.assertEqual(options.new_project, 'new_project')

    def test_boolean_options(self):
        """Test boolean options"""
        options = get_options(['-b', '-u', '-m', '-r'])
        self.assertTrue(options.build)
        self.assertTrue(options.upload)
        self.assertTrue(options.mturk)
        self.assertTrue(options.results)

    def test_config_options(self):
        """Test correct specification of config file"""
        options = get_options(['-c', 'config/configrc'])
        self.assertEqual(options.config_file, 'config/configrc')

    def test_verbosity(self):
        """Test correct specification of verbosity"""
        options = get_options([])
        self.assertEqual(options.debug_level, 0)
        options = get_options(['-v', '1'])
        self.assertEqual(options.debug_level, 1)


class TestMain(unittest.TestCase):

    def setUp(self):
        pass

#    @patch('turkmarker.manage.get_options', side_effect=[
#    def test_new_project(self, shutil_mock, options_mock):
#        """Test copying template files"""

