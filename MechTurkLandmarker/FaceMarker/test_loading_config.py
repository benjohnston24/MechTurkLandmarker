#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
import os
import pandas as pd
import unittest
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import LiveServerTestCase
from MechTurkLandmarker.settings import PAGE_TITLE


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 29 May  16:40:16 AEST 2017'
__license__ = 'MPL v2.0'


class TestLoadingConfigFiles(LiveServerTestCase):

    """ Test the config files are correctly loaded """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.browser = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_page_title(self):
        """Test the page title is correctly loaded"""

        self.browser.get("%s" % self.live_server_url)
        WebDriverWait(self.browser, 20).until(
            EC.title_contains(PAGE_TITLE)) 
