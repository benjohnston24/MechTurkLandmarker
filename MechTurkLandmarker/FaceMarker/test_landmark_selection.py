#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
import os
import pandas as pd
from django.test import LiveServerTestCase
from selenium import webdriver


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 29 May  16:40:16 AEST 2017'
__license__ = 'MPL v2.0'


class TestLandmarkSelection(LiveServerTestCase):

    """ Test correct selection of landmarks """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.localhost = cls.live_server_url
        cls.browser = webdriver.Firefox

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
