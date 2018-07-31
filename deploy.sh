#!/bin/bash
cd /home/pi/gardener
git pull origin master
sudo systemctl stop gardener
echo "Service Stopped"
sudo systemctl start gardener
echo "Service Started"
sudo systemctl status gardener
