# Getting started
```
git clone --recurse-submodules -j8 git@github.com:jmakov/puma-ETL.git
cd puma-ETL && ./scripts/install.sh
```
Define env variables:
* PUMA_SECRETS_PATH
* PUMA_ETL_STAGING_PATH

## Dependencies:
* [puma](https://github.com/jmakov/puma)
* [gulp](https://github.com/jmakov/gulp)
* (optional) [google-drive-ocamlfuse](https://github.com/astrada/google-drive-ocamlfuse/)

# Crontab
Configure crontab to point to bin/crontab-*:
```
0 1 * * 6 /mnt/lvm_volume/dont_delete/workdir/puma/bin/crontab-stop_recorder_and_archive_and_upload.sh
30 0 * * 1 /mnt/lvm_volume/dont_delete/workdir/puma/bin/crontab-start_all_recorders.sh
```


Update AppArmor to allow tcpdump execute post rotate command 
```
sudo aa-complain /usr/sbin/tcpdump
```
# Development
Set `PUMA_DEV_ENV=1`

One approach to filter FIX msgs from [SO](https://stackoverflow.com/questions/13810156/tshark-export-fix-messages):

`tshark -nr <input_file> -Y'fix' -w- | tcpdump -r- -l -w- | tcpflow -r- -C -B`