#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Script to generate the json files that define the number of points
and the correct position within the landmarking system"""

# Imports
import json
import os
import pandas as pd
from utilities import SAVE_FOLDER, LMRKS_FILE
from collections import OrderedDict

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Thursday 1 June  10:36:54 AEST 2017'
__license__ = 'BSD 3-Clause'


CONFIG_JSON = os.path.join(SAVE_FOLDER, "config.json")
CHECK_JS = os.path.join(SAVE_FOLDER, "check.js")

def generate_config_json():
    """Generate a json file containing the number of points"""

    df = pd.read_csv(LMRKS_FILE).values
    num_pts = df.shape[0]
    json_data = OrderedDict() 
    for i in range(num_pts):
        json_data["P%d" % (i + 1)] = {"kind": "point"}

    with open(CONFIG_JSON, 'w') as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    generate_config_json()
