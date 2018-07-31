#!/bin/bash
git pull origin master
sudo systemctl stop gardener
sudo systemctl start gardener
