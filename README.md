# Getting started
```
git clone --recurse-submodules -j8 git@github.com:jmakov/puma-ETL.git
cd puma-ETL && ./scripts/install.sh
```
## Dependencies:
* [puma](https://github.com/jmakov/puma)
* [gulp](https://github.com/jmakov/gulp)

## Tunables
From [Linux TCP tuning](https://www.cyberciti.biz/faq/linux-tcp-tuning/). Also see
[sysctl tweaks](https://wiki.mikejung.biz/Sysctl_tweaks#net.core.netdev_max_backlog)

Set the max OS send buffer size (wmem) and receive buffer size (rmem) to 12 MB for queues on all protocols. In other words set the amount of memory that is allocated for each TCP socket when it is opened or created while transferring files:
```shell script
# echo 'net.core.wmem_max=12582912' >> /etc/sysctl.conf
# echo 'net.core.rmem_max=12582912' >> /etc/sysctl.conf
```
You also need to set minimum size, initial size, and maximum size in bytes:
```shell script
# echo 'net.ipv4.tcp_rmem= 10240 87380 12582912' >> /etc/sysctl.conf
# echo 'net.ipv4.tcp_wmem= 10240 87380 12582912' >> /etc/sysctl.conf
```
Turn on window scaling which can be an option to enlarge the transfer window:
```shell script
# echo 'net.ipv4.tcp_window_scaling = 1' >> /etc/sysctl.conf
```
Enable timestamps as defined in RFC1323:
```shell script
# echo 'net.ipv4.tcp_timestamps = 1' >> /etc/sysctl.conf
```
Enable select acknowledgments:
```shell script
# echo 'net.ipv4.tcp_sack = 1' >> /etc/sysctl.conf
```
Set maximum number of packets, queued on the INPUT side, when the interface receives packets faster than kernel can 
process them.
```shell script
# echo 'net.core.netdev_max_backlog = 1000000' >> /etc/sysctl.conf
```

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