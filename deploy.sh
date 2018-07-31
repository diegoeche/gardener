#!/bin/bash
cd /home/pi/gardener
git pull origin master
sudo systemctl stop gardener
sudo systemctl start gardener
