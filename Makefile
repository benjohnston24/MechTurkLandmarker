# Patterned after Rust-Empty <https://github.com/bvssvni/rust-empty>, MIT License.
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

clean:
	cd MechTurkLandmarker &&\
	rm .coverage &&\
	rm static/lmrk_*.jpg &&\
	rm static/check.js
