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

test:
	coverage xml -i manage.py test --source=${APPS} --omit=${OMIT} --liveserver=localhost:8001-8820
