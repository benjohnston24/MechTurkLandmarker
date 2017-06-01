#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

""" Generate landmark example images """

# Imports
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from MechTurkLandmarker.settings import STATICFILES_DIRS


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Sunday 28 May  21:16:33 AEST 2017'
__license__ = 'BSD 3-Clause'


RADIUS = 3 
BASE_COLOUR = (255, 0, 0) 
HI_COLOUR = (255, 255, 0)
SAVE_FOLDER = STATICFILES_DIRS[0]
UTIL_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FACE = os.path.join(UTIL_FOLDER, "template_face.png")
LMRKS_FILE = os.path.join(UTIL_FOLDER, "template_landmarks.csv")
FONT_FILE = os.path.join(UTIL_FOLDER, 'DejaVuSans.ttf')

SANS16 = ImageFont.truetype(FONT_FILE, 25)

def generate_lmrk_images():
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

        img.save(os.path.join(SAVE_FOLDER,"lmrk_%d.jpg" % (i + 1)))

if __name__ == "__main__":
    generate_lmrk_images()
