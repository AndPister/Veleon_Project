#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import pygame
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

node_type_name = 'tele_operation_node'
pub_twist_name = '/tele_op'

param_config={
    "autonomus_name":"/autonomDrive",
    "stop_name":"/stopp",
    "em_stop_name":"/emergancy_stopp"}

button_config={
    "autonomus_button":0,
    "stop_button":2,
    "em_stop_button":1,
    "rot_axis":0,
    "trans_axsis":3}


max_translat_speed = 6 #m/s
max_rot_speed = 6 #m/s

class joystickinteraktion():

    def __init__(self,pub_twist_name,button_config,param_config):
        self.pub_joy = rospy.Publisher(pub_twist_name, Twist, queue_size=10)
        self.button_config=button_config
        self.param_config=param_config
        self.button_old=[0 for i in range(0,10)]

    def set_twist_info(self,Joystick):
        '''
        Set Controllinput to /tele_op msg
        Input: -- initialized Joystick-obj 
        Output: -- Twist-msg
        '''
        msg = Twist()
        msg.linear.x = Joystick[self.button_config["trans_axsis"]] * max_translat_speed
        msg.angular.z = Joystick[self.button_config["rot_axis"]] * max_rot_speed
        rospy.logdebug(str(msg))
        self.pub_joy.publish(msg)

    def set_param(self,Buttons):
        '''
        Set Controllinput to ROS-Param
        Input: -- initialized Joystick-obj 
        '''

        if self.button_old[self.button_config['em_stop_button']] != Buttons[self.button_config['em_stop_button']] and Buttons[self.button_config['em_stop_button']] ==1:
            new_value= not bool(rospy.get_param(self.button_config['em_stop_button']))
            rospy.set_param(self.param_config['em_stop_name'], str(new_value))

        if self.button_old[self.button_config['stop_button']] != Buttons[self.button_config['stop_button']] and Buttons[self.button_config['stop_button']] ==1:
            new_value= not bool(rospy.get_param(self.button_config['stop_name']))
            rospy.set_param(self.param_config['stop_name'], str(new_value))

        if self.button_old[self.button_config['autonomus_button']] != Buttons[self.button_config['autonomus_button']] and Buttons[self.button_config['autonomus_button']] ==1:
            new_value= not bool(rospy.get_param(self.button_config['autonomus_name']))
            rospy.set_param(self.param_config['autonomus_name'], str(new_value))

        self.button_old = Buttons

    def get_first_param(self):
        '''
        Checks if the parameter are published and set the start value
        '''
        rospy.loginfo("Initial parameter checkup")

        if rospy.has_param(self.param_config['autonomus_name']):
            self.button_old[self.button_config['autonomus_button']]=rospy.get_param(self.param_config['autonomus_name'])
        else:
            rospy.loginfo("Parameter %s couldn’t be found: Using default Value",self.param_config['autonomus_name'])
            rospy.set_param(self.param_config['autonomus_name'], "False")
    
        if rospy.has_param(self.param_config['stop_name']):
            self.button_old[self.button_config['stop_button']]=rospy.get_param(self.param_config['stop_name'])
        else:
            rospy.logwarn("Parameter %s couldn’t be found: Using default Value", self.param_config['stop_name'])
            rospy.set_param(self.param_config['stop_name'], "False")
          
        if rospy.has_param(self.param_config['em_stop_name']):
            self.button_old[self.button_config['em_stop_button']]=rospy.get_param(self.param_config['em_stop_name'])
        else:
            rospy.logwarn("Parameter %s couldn’t be found: Using default Value", self.param_config['em_stop_name'])
            rospy.set_param(self.param_config['em_stop_name'], "False")


    def calback(self,joy):
        '''
        Calbackfunktinon for Joy_node topic
        '''
        set_param(joy.Buttons)
        set_twist_info(joy.axes)

def main():
    '''
    Main function for Controller interaktion
    '''
    joy_obj =joystickinteraktion(pub_twist_name,button_config,param_config)
    joy_obj.get_first_param()#geting first paramsetting from ROS-network
    rospy.init_node(node_type_name,anonymous=False)
    rospy.Subscriber("/Joy", Joy, joy_obj.calback)
    rospy.spin()

try:
    main()   
except rospy.ROSInterruptException as e:
    rospy.logerr("ROS-Error while runung %s : %s",node_type_name,str(e))

except Exception as e:
    rospy.logerr("uncaughed Error while running %s : Errorcode: %s",node_type_name,str(e))




