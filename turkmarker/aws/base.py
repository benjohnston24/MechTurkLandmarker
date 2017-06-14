#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
import boto3

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Wednesday 14 June  09:57:28 AEST 2017'
__license__ = 'MPL v2.0'


class AWSBase(object):
    def __init__(self, config, debug_level=1):
        """Constructor"""

        self.debug_level = debug_level
        self.config = config 
        self.connected = False


