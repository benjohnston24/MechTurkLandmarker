# Patterned after Rust-Empty <https://github.com/bvssvni/rust-empty>, MIT License.
SHELL := /bin/bash

DEFAULT = make help

PROTOCOL_FILES = protocol/protocol.html

all:
	$(DEFAULT)

help:
	clear \
	&& echo "make help            - This help" \
	&& echo "make test            - Execute unittests" \

.PHONY: clean

test:
	cd MechTurkLandmarker &&\
	python manage.py collectstatic --no-input &&\
	python manage.py test --liveserver=localhost:8001-8820 &&\
	cd -
