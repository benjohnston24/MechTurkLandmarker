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
	&& echo "make help            - This help" \
	&& echo "make test            - Execute unittests" \

.PHONY: clean

all: build

build:
	cd MechTurkLandmarker &&\
	python utilities/generate_lmrk_images.py &&\
	python utilities/generate_config_files.py

test: build
	cd MechTurkLandmarker &&\
	nosetests utilities --with-coverage --cover-package=utilities &&\
	coverage xml

clean:
	cd MechTurkLandmarker &&\
	rm .coverage
	rm static/*.jpg
	rm static/check.js
