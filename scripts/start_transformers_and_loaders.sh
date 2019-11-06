#!/usr/bin/env bash

source ~/.profile

/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_pcap.py &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_msgstorage.py &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_backup.py /mnt/backup/data/puma-recorder &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder &
