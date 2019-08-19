#/usr/bin/bash
#
# Script: install-diysystem.sh
# Author: parttimehacker 
# Date:   2019 
# 
# Purpose:fresh install script for Raspberry Pi 
# 
# Notes: get the latest packages and set up file sharing
# 
#!/bin/bash

echo "Welcome to DIY Installation Script diysystem"
echo "This script was modified from a script by LearnOpenCV.com"
echo "================================"
echo "copy and install diysystem.service"
sudo cp diysystem.py /home/an/systemd
sudo cp sysutility.py /home/an/systemd
sudo cp diysystem.service /lib/systemd/system/diysystem.service
sudo chmod 644 /lib/systemd/system/diysystem.service
sudo systemctl daemon-reload
sudo systemctl enable diysystem.service
echo "diysystem.service installation complete"
echo "Reboot recommended"
echo "================================"
echo
