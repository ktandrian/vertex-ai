#!/bin/sh

# Create virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp .env.template .env
