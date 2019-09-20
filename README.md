# Getting started
```
git clone --recurse-submodules -j8 git@github.com:jmakov/puma-ETL.git
cd puma-ETL && ./scripts/install.sh
```
Define env variables:
* PUMA_SECRETS_PATH
* PUMA_ETL_STAGING_PATH

Run extractor that generates 10GB pcap file:
```shell script
/opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py enp1s0 10 &
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
Configure crontab to point to bin/crontab-*:
```
0 10 * * 6 /opt/puma/puma-ETL/scripts/crontab-extractor_stop.sh
30 0 * * 1 /opt/puma/puma-ETL/venv/bin/python3 /opt/puma/puma-ETL/src/extractor.py enp1s0 10
```

# Development
Set `PUMA_DEV_ENV=1`

If using tcpdump:

Update AppArmor to allow tcpdump execute post rotate command 
```
sudo aa-complain /usr/sbin/tcpdump
```

One approach to filter FIX msgs from [SO](https://stackoverflow.com/questions/13810156/tshark-export-fix-messages):

`tshark -nr <input_file> -Y'fix' -w- | tcpdump -r- -l -w- | tcpflow -r- -C -B`