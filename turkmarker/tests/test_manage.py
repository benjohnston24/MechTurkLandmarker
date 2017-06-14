#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
import unittest
from unittest import skip
from unittest.mock import call, patch, MagicMock 
from turkmarker.manage import _main, get_options
from turkmarker.utilities.base import TEMPLATE_DATA

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Wednesday 14 June  16:33:58 AEST 2017'
__license__ = 'BSD 3-Clause'


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

    @patch('shutil.copytree')
    def test_new_project(self, shutil_mock):
        """Test copying template files"""

        _main(['-n', 'new_project'])

        shutil_mock.assert_called_with(TEMPLATE_DATA, 'new_project')

    @patch('turkmarker.manage.get_options')
    @patch('turkmarker.manage.parse_sys_config')
    @patch('turkmarker.manage.GenerateSite')
    @patch('turkmarker.manage.AWSMTurk')
    @patch('turkmarker.manage.AWSS3')
    def test_build_site(self, s3_patch, mturk_patch,
            gen_patch, conf_patch, opt_patch):
        """Test building the site from static file components"""
       
        # Prepare mocks
        class argClass:
            new_project = False 
            build = True
            upload = False 
            mturk = False 
            results = False
            config_file = ''
            debug_level = 0

        opt_patch.side_effect = [argClass]
        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_IMAGE': 'tmp_img.png',
                'TEMPLATE_LANDMARKS': 'tmp_img.csv',
                'BASE_COLOUR': '#ffffff',
                'HI_COLOUR': '#000000',
                'STATIC_FOLDER': 'static',
                'RADIUS': 2,
                }
            }
        conf_patch.side_effect = [config]

        # Generate expected mocks
        expect1 = call(config)
        expect2 = call().generate_lmrk_images(
            image_file=config['LANDMARK-DETAILS']['TEMPLATE_IMAGE'],
            landmarks_file=config['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS'],
            base_colour=config['LANDMARK-DETAILS']['BASE_COLOUR'],
            hi_colour=config['LANDMARK-DETAILS']['HI_COLOUR'],
            save_folder=config['LANDMARK-DETAILS']['STATIC_FOLDER'],
            radius=config['LANDMARK-DETAILS']['RADIUS'],
        )
        expect3 = call().generate_config_json()
        expect4 = call().generate_javascript_check()

        expected_calls = [expect1, expect2, expect3, expect4]

         # Execute 
        _main()
        opt_patch.assert_called_with(None)
        conf_patch.assert_called_with('')
        s3_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        mturk_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        gen_patch.assert_called_with(config)

        # Check the generate functions were called
        self.assertEqual(gen_patch.mock_calls, expected_calls)

        # Check the other methods not called 
        self.assertTrue(call().create_bucket() not in s3_patch.mock_calls)
        self.assertTrue(call().create_external_question_XML(s3_patch().generate_bucket_link()) not in
            mturk_patch.mock_calls)
        self.assertTrue(call().create_HIT(mturk_patch().create_external_question_XML()) not in 
            mturk_patch.mock_calls)
        self.assertTrue(call().list_HITS() not in mturk_patch.mock_calls)

    @patch('turkmarker.manage.get_options')
    @patch('turkmarker.manage.parse_sys_config')
    @patch('turkmarker.manage.GenerateSite')
    @patch('turkmarker.manage.AWSMTurk')
    @patch('turkmarker.manage.AWSS3')
    def test_upload_files(self, s3_patch, mturk_patch,
            gen_patch, conf_patch, opt_patch):
        """Test uploading files to S3"""
       
        # Prepare mocks
        class argClass:
            new_project = False 
            build = False 
            upload = True 
            mturk = False 
            results = False
            config_file = ''
            debug_level = 0

        opt_patch.side_effect = [argClass]

        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_IMAGE': 'tmp_img.png',
                'TEMPLATE_LANDMARKS': 'tmp_img.csv',
                'BASE_COLOUR': '#ffffff',
                'HI_COLOUR': '#000000',
                'STATIC_FOLDER': 'static',
                'RADIUS': 2,
                }
            }
        conf_patch.side_effect = [config]

         # Execute 
        _main()

        opt_patch.assert_called_with(None)
        conf_patch.assert_called_with('')
        s3_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        mturk_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        gen_patch.assert_not_called()

        # Check the S3 functions were called
        self.assertTrue(call().create_bucket() in s3_patch.mock_calls)
        self.assertTrue(call().upload_files() in s3_patch.mock_calls)

        # Check the other methods not called 
        gen_patch.assert_not_called()
        self.assertTrue(call().create_external_question_XML(s3_patch().generate_bucket_link()) not in
            mturk_patch.mock_calls)
        self.assertTrue(call().create_HIT(mturk_patch().create_external_question_XML()) not in 
            mturk_patch.mock_calls)
        self.assertTrue(call().list_HITS() not in mturk_patch.mock_calls)

    @patch('turkmarker.manage.get_options')
    @patch('turkmarker.manage.parse_sys_config')
    @patch('turkmarker.manage.GenerateSite')
    @patch('turkmarker.manage.AWSMTurk')
    @patch('turkmarker.manage.AWSS3')
    def test_mturk_deploy(self, s3_patch, mturk_patch,
            gen_patch, conf_patch, opt_patch):
        """Test deploying to mturk"""
       
        # Prepare mocks
        class argClass:
            new_project = False 
            build = False 
            upload = False 
            mturk = True 
            results = False
            config_file = ''
            debug_level = 0

        opt_patch.side_effect = [argClass]

        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_IMAGE': 'tmp_img.png',
                'TEMPLATE_LANDMARKS': 'tmp_img.csv',
                'BASE_COLOUR': '#ffffff',
                'HI_COLOUR': '#000000',
                'STATIC_FOLDER': 'static',
                'RADIUS': 2,
                }
            }
        conf_patch.side_effect = [config]

         # Execute 
        _main()

        opt_patch.assert_called_with(None)
        conf_patch.assert_called_with('')
        s3_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        mturk_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        gen_patch.assert_not_called()

        # Check the S3 functions were called
        self.assertTrue(call().create_external_question_XML(s3_patch().generate_bucket_link()) in
            mturk_patch.mock_calls)
        self.assertTrue(call().create_HIT(mturk_patch().create_external_question_XML()) in 
            mturk_patch.mock_calls)

        # Check the other methods not called 
        gen_patch.assert_not_called()
        self.assertTrue(call().create_bucket() not in s3_patch.mock_calls)
        self.assertTrue(call().list_HITS() not in mturk_patch.mock_calls)

    @patch('builtins.print')
    @patch('turkmarker.manage.get_options')
    @patch('turkmarker.manage.parse_sys_config')
    @patch('turkmarker.manage.GenerateSite')
    @patch('turkmarker.manage.AWSMTurk')
    @patch('turkmarker.manage.AWSS3')
    def test_mturk_get_results(self, s3_patch, mturk_patch,
            gen_patch, conf_patch, opt_patch, print_patch):
        """Test getting mturk results"""
       
        # Prepare mocks
        class argClass:
            new_project = False 
            build = False 
            upload = False 
            mturk = False 
            results = True 
            config_file = ''
            debug_level = 1

        opt_patch.side_effect = [argClass]

        config = {
            'LANDMARK-DETAILS': {
                'TEMPLATE_IMAGE': 'tmp_img.png',
                'TEMPLATE_LANDMARKS': 'tmp_img.csv',
                'BASE_COLOUR': '#ffffff',
                'HI_COLOUR': '#000000',
                'STATIC_FOLDER': 'static',
                'RADIUS': 2,
                }
            }
        conf_patch.side_effect = [config]

        mturk_patch().list_HITS = MagicMock(side_effect=[[[1],[2]]])
        mturk_patch().save_results_to_file = MagicMock()

         # Execute 
        _main()

        opt_patch.assert_called_with(None)
        conf_patch.assert_called_with('')
        s3_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        mturk_patch.assert_called_with(config=config, debug_level=argClass.debug_level)
        print_patch.assert_called_with("Getting HIT results")

        # Check the mturk functions were called
        self.assertTrue(call().list_HITS() in mturk_patch.mock_calls)
        self.assertTrue(call().save_results_to_file(1) in mturk_patch.mock_calls)
        self.assertTrue(call().save_results_to_file(2) in mturk_patch.mock_calls)

        # Check the other methods not called 
        gen_patch.assert_not_called()
        self.assertTrue(call().create_bucket() not in s3_patch.mock_calls)
        self.assertTrue(call().create_external_question_XML(s3_patch().generate_bucket_link()) not in
            mturk_patch.mock_calls)
        self.assertTrue(call().create_HIT(mturk_patch().create_external_question_XML()) not in 
            mturk_patch.mock_calls)
