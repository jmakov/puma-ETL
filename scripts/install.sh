#!/usr/bin/env bash

INSTALL_PATH=/opt/puma/puma-ETL
SYSCTL_APPEND_COMMAND="sudo tee -a /etc/sysctl.conf"

sudo mkdir -p $INSTALL_PATH/bin

# install dependencies
sudo apt install python3-pip ngrep apparmor-utils python3 python3-venv zstd p7zip-full

sudo cp -r src $INSTALL_PATH

# setup venv
echo "Creating python virtual environment"
sudo python3 -m venv $INSTALL_PATH/venv
source $INSTALL_PATH/venv/bin/activate
sudo $INSTALL_PATH/venv/bin/pip3 install -r requirements.txt

# setup system log dir
sudo mkdir -p /var/log/puma/puma-ETL
sudo chown -R puma:puma /var/log/puma/puma-ETL/

sudo cp scripts/* $INSTALL_PATH/bin

read -p "Tune TCP settings in /etl/sYsctl.conf? [y/n]" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "### Added by puma-ETL ###" | $SYSCTL_APPEND_COMMAND
  echo 'net.core.wmem_max=12582912' | $SYSCTL_APPEND_COMMAND
  echo 'net.core.rmem_max=12582912' | $SYSCTL_APPEND_COMMAND
  echo 'net.ipv4.tcp_rmem= 10240 87380 12582912' | $SYSCTL_APPEND_COMMAND
  echo 'net.ipv4.tcp_wmem= 10240 87380 12582912' | $SYSCTL_APPEND_COMMAND
  echo 'net.ipv4.tcp_window_scaling = 1' | $SYSCTL_APPEND_COMMAND
  echo 'net.ipv4.tcp_timestamps = 1' | $SYSCTL_APPEND_COMMAND
  echo 'net.ipv4.tcp_sack = 1' | $SYSCTL_APPEND_COMMAND
  echo 'net.core.netdev_max_backlog = 1000000' | $SYSCTL_APPEND_COMMAND
  echo "### end of puma-ETL tunables" | $SYSCTL_APPEND_COMMAND

  # apply new settings
  sudo sysctl -p -q
fi
