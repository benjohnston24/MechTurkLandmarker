#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Python build script"""

# Imports
from utilities.generate_lmrk_images import generate_lmrk_images
from utilities.generate_config_files import generate_config_json,\
    generate_javascript_check


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Friday 2 June  13:10:10 AEST 2017'
__license__ = 'BSD 3-clause'

generate_lmrk_images()
generate_config_json()
generate_javascript_check()
