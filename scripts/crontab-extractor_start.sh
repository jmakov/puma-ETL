#!/usr/bin/env bash

source ~/.profile
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py $1 $2
