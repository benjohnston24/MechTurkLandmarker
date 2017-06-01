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

build:
	python utilities/generate_lmrk_images.py
	python utilities/generate_config_files.py
	python manage.py collectstatic --no-input

test:
	COVERAGE_FILE=.django_coverage coverage run --source=${APPS} --omit=${OMIT} manage.py test 
	COVERAGE_FILE=.utils_coverage nosetests utilities --with-coverage --cover-package=utilities
	coverage combine .django_coverage .utils_coverage
	coverage xml

run:
	python manage.py collectstatic --no-input
	python manage.py runserver


clean:
	rm static/*.jpg
	rm static/check.js
	rm staticfiles/*.*
