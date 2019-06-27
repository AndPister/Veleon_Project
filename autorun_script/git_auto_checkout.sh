#!/bin/bash
#
#This script covers all launch and autorunfunction of the veleon_project

if ping -q -c 1 -W 1 google.com >/dev/null; then
  echo "positiv internet-connetion"
  eval $(ssh-agent -s)
  ssh-add
  cd home/pi/Veleon_Project
  sleep 5
  git pull origin master
  #git fetch origin
  #sleep 5
  #git reset --hard origin/master
else
  echo "internet is not available!! \nNo update was done"
fi

exit 0
