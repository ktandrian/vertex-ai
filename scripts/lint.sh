#!/bin/sh
source .venv/bin/activate
pip install pylint
pylint **/*.py
