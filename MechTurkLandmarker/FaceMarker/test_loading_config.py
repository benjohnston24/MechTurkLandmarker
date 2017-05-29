#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
import os
import pandas as pd
import unittest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MechTurkLandmarker.settings import PAGE_TITLE


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 29 May  16:40:16 AEST 2017'
__license__ = 'MPL v2.0'


class TestLoadingConfigFiles(StaticLiveServerTestCase):

    """ Test the config files are correctly loaded """

    @classmethod
    def setUpClass(cls):
        super(TestLoadingConfigFiles, cls).setUpClass()

        cls.browser = WebDriver()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(TestLoadingConfigFiles, cls).tearDownClass()

    def test_page_title(self):
        """Test the page title is correctly loaded"""

        print(self.live_server_url)
        self.browser.get("%s" % self.live_server_url)
        WebDriverWait(self.browser, 10).until(
           EC.title_contains(PAGE_TITLE)) 
