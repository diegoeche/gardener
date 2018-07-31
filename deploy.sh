#!/bin/bash
cd /home/pi/gardener
git pull origin master
sudo systemctl stop gardener
echo "Service Stoped"
sudo systemctl start gardener
echo "Service Started"
sudo systemctl status gardener
