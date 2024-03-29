#!/usr/bin/env bash

INSTALL_PATH=/opt/puma-ETL

sudo rm -rf $INSTALL_PATH/venv
sudo mkdir -p $INSTALL_PATH

# install dependencies
sudo add-apt-repository ppa:alessandro-strada/ppa -y
sudo apt-get update
sudo apt-get install google-drive-ocamlfuse python3-pip ngrep python3 python3-venv zstd p7zip-full -y

sudo cp -rf src $INSTALL_PATH
sudo cp -rf scripts $INSTALL_PATH

# setup venv
echo "Creating python virtual environment"
sudo python3 -m venv $INSTALL_PATH/venv
source $INSTALL_PATH/venv/bin/activate
sudo $INSTALL_PATH/venv/bin/pip3 install wheel
sudo $INSTALL_PATH/venv/bin/pip3 install -r requirements.txt

# setup system log dir
sudo mkdir -p /var/log/puma-ETL
sudo chown root:puma /var/log/puma-ETL
sudo chmod 755 /var/log/puma-ETL
