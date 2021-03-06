#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
#Project:       Veleon-Project
#Subproject:    Teleoperation 
#Autor:         Andreas Pister
#Date:          09.07.2019
#
#Discription:   This Script covers the Teleoperationnode of the 
#               Veleon-Bike. Also it includes the communication betwen the 
#               Joy-message and the motioncontole.
#
#Input:         /joy-Topic : covers the inpot of the XBox-controler
#               
#Output:        /tele_op: the Teleoperation-topic
#               /autonomDrive-Parameter: indicates the Mode of autonomic driving
#               /stopp-Parameter: indicates the Mode of stopping the System
#               /emergancy_stopp: indicates the Mode of fullsoping all procsses
#
#########################################################################
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

node_name = 'tele_operation_node'
pub_twist_name = '/tele_op'
sub_joy_name = '/joy'

param_config={
    "autonomus_name":'/autonomDrive',
    "stop_name":'/stopp',
    "em_stop_name":'/emergancy_stopp',
    "rot_multiply":'~/tele_operation_node/max_rotation_speed',
    "trans_multiply":'~/tele_operation_node/max_translatory_speed'}

button_config={
    "autonomus_button":0,
    "stop_button":2,
    "em_stop_button":1,
    "rot_axis":0,
    "trans_axsis":3}


default_max_translat_speed = 6 #m/s
default_max_rot_speed = 6 #m/s

class joystickinteraktion():
    
    def __init__(self,pub_twist_name,sub_joy_name,button_config,param_config):
        rospy.init_node(node_name,anonymous=False,log_level=rospy.INFO) 
        rospy.Subscriber(sub_joy_name, Joy, self.callback)
        self.pub_teleop = rospy.Publisher(pub_twist_name, Twist, queue_size=2)
        self.button_config=button_config
        self.param_config=param_config
        self.button_old=[0 for i in range(0,10)]
        self.default_max_translat_speed = 6 #m/s
        self.default_max_rot_speed = 6 #m/s
        self.msg=Twist()

    def set_twist_info(self,Joystick):
        '''
        Set ContrSollinput to /tele_op msg
        Input: -- initialized Joystick-obj 
        Output: -- Twist-msg
        '''
        
        self.msg.linear.x = Joystick[self.button_config["trans_axsis"]]*rospy.get_param(self.param_config['trans_multiply'],self.default_max_translat_speed)
        self.msg.angular.z = Joystick[self.button_config["rot_axis"]]*rospy.get_param(self.param_config['rot_multiply'],self.default_max_rot_speed)

    def set_param_values(self,Buttons):
        '''
        Set Controllinput to ROS-Param
        Input: -- initialized Joystick-obj 
        '''

        if self.button_old[self.button_config['em_stop_button']] != Buttons[self.button_config['em_stop_button']] and Buttons[self.button_config['em_stop_button']] ==1:
            new_value= not bool(rospy.get_param(self.param_config['em_stop_name'],True))
            rospy.logdebug("%s: %s",self.param_config['em_stop_name'], new_value)
            rospy.set_param(self.param_config['em_stop_name'],new_value)

        if self.button_old[self.button_config['stop_button']] != Buttons[self.button_config['stop_button']] and Buttons[self.button_config['stop_button']] ==1:
            new_value= not bool(rospy.get_param(self.param_config['stop_name'],True))
            rospy.logdebug("%s: %s",self.param_config['stop_name'], new_value)
            rospy.set_param(self.param_config['stop_name'],new_value)

        if self.button_old[self.button_config['autonomus_button']] != Buttons[self.button_config['autonomus_button']] and Buttons[self.button_config['autonomus_button']] ==1:
            new_value= not bool(rospy.get_param(self.param_config['autonomus_name'],True))
            rospy.logdebug("%s: %s",self.param_config['autonomus_name'], new_value)
            rospy.set_param(self.param_config['autonomus_name'], new_value)

        self.button_old = Buttons

    def get_first_param(self):
        '''
        Checks if the parameter are published and set the start value
        '''
        rospy.loginfo("Initial parameter checkup")

        if rospy.has_param(self.param_config['autonomus_name']):
            self.button_old[self.button_config['autonomus_button']]=rospy.get_param(self.param_config['autonomus_name'])
        else:
            rospy.logwarn("Parameter %s couldn’t be found: Using default Value",self.param_config['autonomus_name'])
            rospy.set_param(self.param_config['autonomus_name'], False)
    
        if rospy.has_param(self.param_config['stop_name']):
            self.button_old[self.button_config['stop_button']]=rospy.get_param(self.param_config['stop_name'])
        else:
            rospy.logwarn("Parameter %s couldn’t be found: Using default Value", self.param_config['stop_name'])
            rospy.set_param(self.param_config['stop_name'], False)
          
        if rospy.has_param(self.param_config['em_stop_name']):
            self.button_old[self.button_config['em_stop_button']]=rospy.get_param(self.param_config['em_stop_name'])
        else:
            rospy.logwarn("Parameter %s couldn’t be found: Using default Value", self.param_config['em_stop_name'])
            rospy.set_param(self.param_config['em_stop_name'], False)

    def callback(self,joy):
        '''
        Callbackfunktinon for Joy_node topic
        '''  
        self.set_param_values(joy.buttons)
        self.set_twist_info(joy.axes)
    
    def run (self):
        rate=rospy.Rate(20)
        while not rospy.is_shutdown():
            rospy.logdebug(self.msg)
            self.pub_teleop.publish(self.msg)
            rate.sleep()    

try:
    joy_obj =joystickinteraktion(pub_twist_name,sub_joy_name,button_config,param_config)
    joy_obj.run()  
except rospy.ROSInterruptException as e:
    rospy.logerr("ROS-Error while runung %s : %s",node_name,str(e))

except Exception as e:
    rospy.logerr("Uncaughed error while running %s : Errorcode: %s",node_name,str(e))




