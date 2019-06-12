#!/bin/bash

##############################################
#           Basic Install Script
#
#Project:       Veleon-Project
#Subproject:    Basic Install Script
#Autor:         Andreas Pister
#Date:          16.05.19
#Discription:   This Script covers the Main install 
#               
#               joy_pkg


#Set Configure to .bashrc
echo "Set Configure to .bashrc"
_IMPORTSTRING="
#sourceing workspace\n
source ~/Veleon_Project/catkin_ws/devel/setup.bash\n
\n
#set ROS Master\n
export ROS_MASTER_URI=http://192.168.9.212:11311\n
#if you use a Virtual-Maschiene to connekt to Bike, you have to setup your IP manuel\n
export ROS_HOSTNAME=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)\n
\n
#error-fix gazebo with VM\n
export SVGA_VGPU10=0\n
"

_IP = arp -na | grep -i b8:27:eb
echo $_IP
echo -e $_IMPORTSTRING >> ~/.bashrc



echo "Install Joy-Package"
#installing Joy_pkg for Connecting to to xBox-controler
sudo apt-get install ros-kinetic-joy
#sudo chmod a+rw /dev/input/js0

exit 0
