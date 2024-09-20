#!/bin/bash
echo "BUILD START"

# Upgrade pip and install requirements
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade -r requirements.txt --disable-pip-version-check --no-cache-dir

echo "BUILD END"
