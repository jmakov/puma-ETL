#!/usr/bin/env bash

INSTALL_PATH=/opt/puma/puma-ETL
SYSCTL_APPEND_COMMAND="sudo tee -a /etc/sysctl.conf"

sudo mkdir -p $INSTALL_PATH/bin

# install dependencies
sudo apt install python3-pip ngrep python3 python3-venv zstd p7zip-full

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
