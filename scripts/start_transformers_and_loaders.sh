#!/usr/bin/env bash

/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/transformer_pcap.py &
/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/transformer_msgstorage.py &
/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/loader_backup.py /pool_raidz1_3_12TB/data/puma-recorder &
/opt/puma-ETL/venv/bin/python3 /opt/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder &
