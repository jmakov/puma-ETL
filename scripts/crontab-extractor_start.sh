#!/usr/bin/env bash

source ~/.profile

/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/extractor.py $1 $2
