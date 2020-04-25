# Getting started
1. Clone the repo 
    ```shell script
    git clone --recurse-submodules -j8 git@github.com:jmakov/puma-ETL.git
    cd puma-ETL && ./scripts/install.sh
    ```
2. copy `examples/feeds.yaml` and `examples/puma-ETL.yaml` to `/etc/puma/` and edit them
3. set file permissions
    ```shell script
    sudo chown root:puma /etc/puma/*
    sudo chmod 640 /etc/puma*
    ```
4. set staging directory e.g. `/mnt/staging` permissions
    ```shell script
    sudo chown -R puma:puma /mnt/staging
    sudo chmod -R 755 /mnt/staging
    ```
# Usage
```shell script
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py enp1s0 &
```

Start transformers that backup to `/mnt/backup` and archive to `/mnt/gdrive/project_data/puma-recorder`:
```shell script
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_pcap.py &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/transformer_msgstorage.py &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_backup.py /mnt/backup &
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/loader_archive.py /mnt/gdrive/project_data/puma-recorder
```
## Dependencies:
* [puma](https://github.com/jmakov/puma)
* [gulp](https://github.com/jmakov/gulp)
* (optional) [google-drive-ocamlfuse](https://github.com/astrada/google-drive-ocamlfuse/)

# Crontab
Config crontab for user `puma`: `sudo crontab -u puma -e
```shell script
1 0 * * 1 /opt/puma/puma-ETL/scripts/crontab-extractor_stop.sh
2 0 * * 1 /opt/puma/puma-ETL/scripts/crontab-extractor_start.sh enp1s0
```

# Development
1. `$ export PUMA_DEV_ENV=1`.
2. copy `examples/feeds.yaml` and `examples/puma-ETL.yaml` to project root and edit them 

If using tcpdump:

Update AppArmor to allow tcpdump execute post rotate command 
```shell script
sudo aa-complain /usr/sbin/tcpdump
```

One approach to filter FIX msgs from [SO](https://stackoverflow.com/questions/13810156/tshark-export-fix-messages):

`tshark -nr <input_file> -Y'fix' -w- | tcpdump -r- -l -w- | tcpflow -r- -C -B`