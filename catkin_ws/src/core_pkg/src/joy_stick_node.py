#!/usr/bin/env python
import rospy
import pygame
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

node_type_name = "/joy_stick_node"
pub_twist_name = "/tele_op"

param_config={
    "joystick_con_name":"/controller_connected",
    "autonomus_name":"/autonomDrive",
    "stop_name ":"/stopp",
    "em_stop_name":"/emergancy_stop"
}

button_config={
    "autonomus_button":1,
    "stop_button":1,
    "em_stop_button":1,
    "rot_axis":1,
    "trans_axsis":1
}


max_translat_speed = 6 #m/s
max_rot_speed = 6 #m/s

class joystickinteraktion:

    def __init__(pub_twist_name,button_config,param_config):
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

        if self.button_old[self.button_config["em_stop_button"]] != Buttons[self.button_config["em_stop_button"]] and Buttons[self.button_config["em_stop_button"]] ==1:
            new_value= not bool(rospy.get_param(self.button_config["em_stop_button"])
            rospy.set_param(self.param_config["em_stop_name"], str(new_value))

        if self.button_old[self.button_config["stop_button"]] != Buttons[self.button_config["stop_button"]] and Buttons[self.button_config["stop_button"]] ==1:
            new_value= not bool(rospy.get_param(self.button_config["stop_button"])
            rospy.set_param(self.param_config["stop_name"], str(new_value))

        if self.button_old[self.button_config["autonomus_button"]] != Buttons[self.button_config["autonomus_button"]] and Buttons[self.button_config["autonomus_button"]] ==1:
            new_value= not bool(rospy.get_param(self.button_config["autonomus_button"])
            rospy.set_param(self.param_config["autonomus_name"], str(new_value))

        self.button_old = Buttons

    def get_first_param(self):
    '''
    Checks if the parameter are published and set the start value
    '''
    rospy.loginfo("Initial parameter checkup ")

    if rospy.has_param(para_autonomus_name):
        self.button_old[self.button_config["autonomus_button"]] = int(rospy.get_param(para_autonomus_name)) 
    else:
        rospy.loginfo(para_autonomus_name + "couldn’t be found: Using default Value")

        
    if rospy.has_param(para_stop_name):
        self.button_old[self.button_config["stop_button"]] = int(rospy.get_param(para_stop_name))
    else:
        rospy.logwarn(para_stop_name + "couldn’t be found: Using default Value")

        
    if rospy.has_param(para_em_stop_name):
        self.button_old[self.button_config["em_stop_button"]] = int(rospy.get_param(para_em_stop_name))
    else:
        rospy.logwarn(para_em_stop_name + "couldn’t be found: Using default Value")


    def calback(self,joy):
        '''
        Calbackfunktinon for Joy_node topic
        '''
        set_param(joy.Buttons)
        set_twist_info(joy.axes)

def main():
    '''
    Main function for Controller integration
    '''
    joy_obj =joystickinteraktion(pub_twist_name,button_config,param_config)
    joy_obj.get_first_param()#geting first paramsetting from ROS-network
    rospy.init_node(node_type_name, anonymous=True)
    rospy.Subscriber("/Joy", Joy, joy_obj.calback)
    rospy.range(50).sleep()
    rospy.spin()

if __name__ == "__main__":
    try:
        main()   
    except Exception as e:
        rospy.logerr("Error while running joy_stick_node Errorcode:"+str(e))



