#!/bin/bash
#
#This script covers all launch and autorunfunction of the veleon_project

echo "source ROS"
source /opt/ros/kinetic/setup.bash
_IP=$(hostname -I)||true

echo "Setup ROS-Master"
#export ROS_MASTER_URI=http://$_IP:11311 | xargs
#export ROS_HOSTNAME=$_IP | xargs
export ROS_MASTER_URI=http://192.168.9.212:11311
export ROS_HOSTNAME=192.168.9.212
echo $ROS_MASTER_URI
echo $ROS_HOSTNAME

echo "Build workspace"
cd home/pi/Veleon_Project/catkin_ws
catkin_make
#/home/pi/Veleon_Project/catkin_ws

echo "source workspace"
source /home/pi/Veleon_Project/catkin_ws/devel/setup.bash

echo "ROS ready to start"
sleep 5

echo "Launch ROS"
roslaunch core_pkg core_launch.launch

exit 0
