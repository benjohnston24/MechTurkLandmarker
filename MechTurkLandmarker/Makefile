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
	python manage.py collectstatic --no-input
	COVERAGE_FILE=.django_coverage coverage run --source=${APPS} --omit=${OMIT} manage.py test 
	COVERAGE_FILE=.utils_coverage nosetests utilities --with-coverage --cover-package=utilities
	coverage combine .django_coverage .utils_coverage
	coverage xml
