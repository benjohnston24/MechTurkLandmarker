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
	cd turkmarker && python turkmarker.py -b
#		python -m markdown -o html protocol.md > protocol.html

test: 
	cd turkmarker &&\
		MECHTURK_ID=1234 MECHTURK_KEY=456 nosetests --with-coverage --cover-package=turkmarker &&\
		coverage xml -i

upload:
	cd turkmarker &&\
		python turkmarker.py -u -v 1

create_hit:
	cd turkmarker &&\
		python turkmarker.py -m -v 1

hit_results:
	cd turkmarker &&\
		python turkmarker.py -r -v 1

clean:
	cd turkmarker &&\
	rm .coverage &&\
	rm static/lmrk_*.jpg &&\
	rm static/check.js
