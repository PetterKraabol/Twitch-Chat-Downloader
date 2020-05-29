#!/usr/bin/env bash

./setup.py sdist bdist_wheel
twine upload dist/*
