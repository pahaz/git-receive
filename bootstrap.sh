#!/bin/bash

apt-get install python3-pip
apt-get install sshcommand

PYTHON=$(which python3)

$PYTHON -m pip install -U gitreceive

