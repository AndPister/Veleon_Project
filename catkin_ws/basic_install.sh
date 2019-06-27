#!/bin/bash

##############################################
#           Basic Install Script
#
#Project:       Veleon-Project
#Subproject:    Basic Install Script
#Autor:         Andreas Pister
#Date:          16.05.19
#Discription:   This Script covers the Main install 
#               ROS Configuration
#               VM-Bugfix 
#               joy_pkg

#install ros 
#sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
#sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
#sudo apt-get update
#sudo apt-get install ros-kinetic-desktop-full -y
#sudo rosdep init
#rosdep update
#echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
#source ~/.bashrc
#sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential -y

#Set Configure to .bashrc
echo "Set Configure to .bashrc"
_ROSIMPORT="
#sourceing workspace\n
source ~/Veleon_Project/catkin_ws/devel/setup.bash\n
\n
#set ROS Master\n
export ROS_MASTER_URI=http://192.168.9.212:11311\n
#if you use a Virtual-Maschiene to connekt to Bike, you have to setup your IP manuel\n
export ROS_HOSTNAME=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)\n
"
echo -e $_ROSIMPORT >> ~/.bashrc

echo "Fix VM-Error!"
_VMIMPORT"
#error-fix gazebo with VM\n
export SVGA_VGPU10=0\n
"
echo -e $_VMIMPORT >> ~/.bashrc

echo "Install Joy-Package"
#installing Joy_pkg for Connecting to to xBox-controler
sudo apt-get install xboxdrv
#sudo apt-get install ros-kinetic-joy
#sudo chmod a+rw /dev/input/js0
sudo apt install python3-pip -y
python3 -m pip install -U pygame --user

exit 0