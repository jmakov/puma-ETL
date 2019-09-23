#!/usr/bin/env bash

/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py enp1s0 100
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_pcap.py &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_msgstorage.py &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_backup.py /mnt/backup/data/puma-recorder &
#/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_backup.py /home/toaster/staging/backup /home/toaster/staging/loader_backup /home/toaster/staging/transformer_pcap /home/toaster/staging/transformer_msgstorage &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder &
#/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder /home/toaster/staging/loader_archive /home/toaster/staging/loader_backup &
