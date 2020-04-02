#!/bin/bash

set -e

git fetch upstream
git merge upstream/master --no-edit

echo "Updating CSVs..."

python3 transform.py

echo "Normalized CSVs updated."

