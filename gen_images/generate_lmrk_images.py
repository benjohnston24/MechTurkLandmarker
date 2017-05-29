#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

""" Generate landmark example images """

# Imports
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Sunday 28 May  21:16:33 AEST 2017'
__license__ = 'MPL v2.0'


TEMPLATE_FACE = "template_face.png"
RADIUS = 3 
BASE_COLOUR = (255, 0, 0) 
HI_COLOUR = (255, 255, 0)

sans16 = ImageFont.truetype(
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 25)

# Load landmarks
lmrks = pd.read_csv('template_landmarks.csv').values


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
        fill=HI_COLOUR, font=sans16)

    img.save("lmrk_%d.jpg" % (i + 1))
