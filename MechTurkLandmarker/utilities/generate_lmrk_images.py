#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

""" Generate landmark example images """

# Imports
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from utilities.base import parse_sys_config, UTIL_FOLDER,\
    DEFAULT_SYS_CONFIG


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Sunday 28 May  21:16:33 AEST 2017'
__license__ = 'BSD 3-Clause'

FONT_FILE = os.path.join(UTIL_FOLDER, 'DejaVuSans.ttf')
SANS16 = ImageFont.truetype(FONT_FILE, 25)

def generate_lmrk_images(config_file=DEFAULT_SYS_CONFIG):
    """Generate the images to indicate the current point to be landmarked"""

    config = parse_sys_config(config_file)

    LMRKS_FILE = config['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS']
    TEMPLATE_FACE = config['LANDMARK-DETAILS']['TEMPLATE_FACE']
    BASE_COLOUR = config['LANDMARK-DETAILS']['BASE_COLOUR']
    HI_COLOUR = config['LANDMARK-DETAILS']['HI_COLOUR']
    SAVE_FOLDER = config['LANDMARK-DETAILS']['STATIC_FOLDER']
    RADIUS = int(config['LANDMARK-DETAILS']['RADIUS'])

    # Load landmarks
    lmrks = pd.read_csv(LMRKS_FILE).values

    # Iterate through all landmarks
    for i in range(lmrks.shape[0]):
        img = Image.open(TEMPLATE_FACE)
        draw = ImageDraw.Draw(img)
        # Plot all the points
        for pts in lmrks:
            draw.ellipse((
                pts[0] - (RADIUS / 2), pts[1] - (RADIUS / 2),
                pts[0] + RADIUS, pts[1] + RADIUS),
                fill=BASE_COLOUR)

        pts = lmrks[i]
        draw.ellipse((
            pts[0] - (RADIUS / 2), pts[1] - (RADIUS / 2),
            pts[0] + RADIUS, pts[1] + RADIUS),
            fill=HI_COLOUR)
        draw.text((pts[0] - 2 * RADIUS, pts[1]),
            "P%d" % (i + 1),
            fill=HI_COLOUR, font=SANS16)

        draw.text((10, 10),
            "DO NOT CLICK ON THIS IMAGE",
            fill=BASE_COLOUR, font=SANS16)

        img.save(os.path.join(SAVE_FOLDER,"lmrk_P%d.jpg" % (i + 1)))

if __name__ == "__main__":
    generate_lmrk_images()
