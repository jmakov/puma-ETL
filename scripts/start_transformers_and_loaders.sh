#!/usr/bin/env bash

# /opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py enp1s0 100
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py enp111s0 1
sleep 1 # make time for dir creation
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_pcap.py &
sleep 1 # make time for dir creation
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_msgstorage.py &
sleep 1 # make time for dir creation
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_backup.py /mnt/backup/project_data/puma-recorder &
sleep 1 # make time for dir creation
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder &
