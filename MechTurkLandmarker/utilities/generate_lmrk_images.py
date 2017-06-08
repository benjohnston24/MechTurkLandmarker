#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

""" Generate landmark example images """

# Imports
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from utilities.base import UTIL_FOLDER 

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Sunday 28 May  21:16:33 AEST 2017'
__license__ = 'BSD 3-Clause'

FONT_FILE = os.path.join(UTIL_FOLDER, 'DejaVuSans.ttf')
SANS16 = ImageFont.truetype(FONT_FILE, 25)

def generate_lmrk_images(image_file, landmarks_file, base_colour, hi_colour, save_folder, radius):
    """Generate the images to indicate the current point to be landmarked"""

    # Load landmarks
    lmrks = pd.read_csv(landmarks_file).values

    # Iterate through all landmarks
    for i in range(lmrks.shape[0]):
        img = Image.open(image_file)
        draw = ImageDraw.Draw(img)
        # Plot all the points
        for pts in lmrks:
            draw.ellipse((
                pts[0] - (radius / 2), pts[1] - (radius / 2),
                pts[0] + radius, pts[1] + radius),
                fill=base_colour)

        pts = lmrks[i]
        draw.ellipse((
            pts[0] - (radius / 2), pts[1] - (radius / 2),
            pts[0] + radius, pts[1] + radius),
            fill=hi_colour)
        draw.text((pts[0] - 2 * radius, pts[1]),
            "P%d" % (i + 1),
            fill=hi_colour, font=SANS16)

        draw.text((10, 10),
            "DO NOT CLICK ON THIS IMAGE",
            fill=base_colour, font=SANS16)

        img.save(os.path.join(save_folder,"lmrk_P%d.jpg" % (i + 1)))
