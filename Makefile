#!/bin/bash
# Ben Johnston
# Wednesday 7 June  15:06:32 AEST 2017
# License BSD 3-Clause
# Variables ###################################################################
SHELL := /bin/bash

DEFAULT = make help

PROTOCOL_FILES = protocol/protocol.html

APPS=FaceMarker,MechTurkLandmarker
OMIT=*/test*.py,*/migrations/*.py

###############################################################################

all:
	$(DEFAULT)

help:
	clear \
	&& echo "make help - This help" \
	&& echo "make test - Execute unittests" \

.PHONY: clean

all: build

build:
	cd MechTurkLandmarker && python build_utils.py &&\
		python -m markdown -o html protocol.markdown > protocol.html

test: 
	cd MechTurkLandmarker &&\
		MECHTURK_ID=1234 MECHTURK_KEY=456 nosetests -s --with-coverage --cover-package=utilities &&\
		coverage xml -i

upload:
	cd MechTurkLandmarker &&\
		python deploy.py -u -d 1

create_hit:
	cd MechTurkLandmarker &&\
		python deploy.py -m -d 1

hit_results:
	cd MechTurkLandmarker &&\
		python deploy.py -r -d 1

clean:
	cd MechTurkLandmarker &&\
	rm .coverage &&\
	rm static/lmrk_*.jpg &&\
	rm static/check.js
