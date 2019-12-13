#!/usr/bin/env bash

source ~/.profile

/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/transformer_pcap.py &
/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/transformer_msgstorage.py &
/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/loader_backup.py /mnt/raid0/data/puma-recorder &
/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder &
