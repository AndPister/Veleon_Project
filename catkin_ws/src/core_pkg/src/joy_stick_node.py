#!/usr/bin/env python
import rospy
import pygame
from geometry_msgs.msg import Twist

node_type_name = "/joy_stick_node"
pub_twist_name = "/tele_op"
para_joystick_con_name ="/controller_connected"
para_autonomus_name = "/autonomDrive"
para_stop_name = "/stopp"
para_em_stop_name = "/emergancy_stop"

nr_autonomus_button = 1
nr_stop_button = 2
nr_em_stop_button = 3
nr_rot_axis =1
nr_trans_axsis = 3

autonomus_button_old = False
stop_button_old = False
em_stop_button_old = False

max_translat_speed = 6 #m/s
max_rot_speed = 6 #m/s


def get_twist_info(Joystick):
    '''
    Set Controllinput to /tele_op msg
    Input: -- initialized Joystick-obj 
    Output: -- Twist-msg
    '''

    msg = Twist()
    msg.linear.x = Joystick.pygame.joystick.get_axis(nr_trans_axsis) * max_translat_speed
    msg.angular.z = Joystick.pygame.joystick.get_axis(nr_rot_axis) * max_rot_speed

    return msg

def set_param(Joystick):
    '''
    Set Controllinput to ROS-Param
    Input: -- initialized Joystick-obj 
    '''

    if Joystick.get_button(nr_em_stop_button)==1:
        em_stop_button_old = not em_stop_button_old
        rospy.set_param(para_em_stop_name, str(em_stop_button_old))

    if Joystick.get_button(nr_autonomus_button)==1:
        autonomus_button_old = not autonomus_button_old
        rospy.set_param(para_autonomus_name, str(autonomus_button_old))

    if Joystick.get_button(nr_stop_button)==1:
        stop_button_old = not stop_button_old
        rospy.set_param(para_stop_name, str(stop_button_old))

#def get_first_param():
 #   '''
  #  Checks if the parameter are published and set the start value
   # '''
#
 #   rospy.loginfo("Initial parameter checkup ")
#
#
 #   if rospy.has_param(para_autonomus_name):
  #      autonomus_button_old = rospy.get_param(para_autonomus_name) 
   # else:
    #    #rospy.loginfo(para_autonomus_name + "couldn’t be found: Using default Value")
     #   autonomus_button_old = False
    #
    #if rospy.has_param(para_stop_name):
    #    stop_button_old = rospy.get_param(para_stop_name)
    #else:
    #    #rospy.logwarn(para_stop_name + "couldn’t be found: Using default Value")
    #    stop_button_old = False
    #    
    #if rospy.has_param(para_em_stop_name):
    #    em_stop_button_old = rospy.get_param(para_em_stop_name)
    #else:
    #    #rospy.logwarn(para_em_stop_name + "couldn’t be found: Using default Value")
     #   em_stop_button_old = False

def main():
    '''
    Main function for Controller integration
    '''

    rospy.loginfo("initial controllerrequest")
    #initial controllerrequest
    pygame.pygame.init()
    while pygame.joystick.get_init() <=0: #check if controller is available
        pygame.pygame.quit()
        pygame.pygame.init()

    Joystick = pygame.joystick.Joystick(0)
    Joystick.init()

    rospy.set_param(para_joystick_con,"True")

    get_first_param()#geting first paramsetting from ROS-network

    pub_joy = rospy.Publisher(pub_twist_name, Twist, queue_size=10)
    rospy.init_node(node_type_name, anonymous=True)
    
    while not rospy.is_shutdown():
        data = get_twist_info(Joystick)
        set_param(Joystick)
        pub_joy.publish(data)        
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()   
    except Exception as e:
        rospy.logerr("Error while running joy_stick_node Errorcode:"+str(e))






