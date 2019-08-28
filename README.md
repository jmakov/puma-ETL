# Getting started
```
git clone --recurse-submodules -j8 git@github.com:jmakov/puma-ETL.git
cd puma-ETL && ./scripts/install.sh
```

## Dependencies:
* [puma](https://github.com/jmakov/puma)
* [gulp](https://github.com/jmakov/gulp)

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