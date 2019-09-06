#!/usr/bin/env bash

/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_pcap.py
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_msgstorage.py
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_backup.py /mnt/backup
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder/
