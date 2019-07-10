#!/usr/bin/env python

#########################################################################
#Project:       Veleon-Project
#Subproject:    Kinematic and Actor-Comunicatiion 
#Autor:         Andreas Pister
#Date:          10.05.19
#
#Discription:   This Script covers the MotionControle of the 
#               Veleon-Bike. Also it includes the kinimatic mathematics 
#               and the Actor-Comunication.
#
#Input:         /cmd_vel-Topic : covers the motion-trjectoris
#               /motion_controle/simulation_enable -Param : covers the 
#                   switch between Simulation and real communication
#Output:        Output will be several inforation about the Actors and 
#                   motioninput. Also it will publish the truth of the 
#                   /cmd_vel input
#########################################################################
        


import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray
from bike_services_pkg.srv import i2c_service

enable_param = '/motion_controle/simulation_enable'
node_name = 'motion_controle_node'
wheel_pub_name = '/motion_controle/wheel_speed'
service_name='i2c_service'
motor_interface_addr= 42
x_dot_default = 0.0
alpha_dot_default = 0.0


R = 0.503         
d = 0.77/2

def kinematics(cmd_vel):
    '''
    This Funktion includes the kinematic mathematics.
    Input: cmd_vel-content
    Output: phi_dot
    '''
    x_dot = cmd_vel.linear.x
    alpha_dot = cmd_vel.angular.z 
    
    #check if join-angle is in Tolerance
    if rospy.get_param('/emergancy_stopp',False): 
        phi_dot_r = (x_dot+d*alpha_dot)/R
        phi_dot_l = (x_dot-d*alpha_dot)/R
    elif rospy.get_param('/emergancy_stopp'):
        rospy.logerr("Emergency stop is active ")
        phi_dot_r = 0
        phi_dot_l = 0
    else:
        rospy.logerr("Circle to small !! Default Values are used!! x_dot: %s alpha_dot:%s",x_dot_default,alpha_dot_default)
        phi_dot_r = 0
        phi_dot_l = 0
    return [phi_dot_l, phi_dot_r]

def listener():
    rospy.init_node(node_name,anonymous=False)
    topic_name ='/tele_op'
    rospy.logdebug("Used Topic: %s", topic_name)
    while not rospy.is_shutdown():
        topic_name = check_topic(topic_name)
        rospy.Subscriber(topic_name, Twist, calback)
        
def calback(data):
    phi_dot = kinematics(data)

    rospy.logdebug(phi_dot)

def check_topic(old_value):
    topic_name = '/tele_op'

    if rospy.get_param('/autonomDrive',False):
        topic_name = '/cmd_vel'
    else:
        topic_name = '/tele_op'

    if topic_name != old_value:
        rospy.logdebug("Used Topic has changed to: %s", topic_name)
    
    return topic_name

def send_phi(phi_dots):
    rospy.wait_for_service(service_name)
    try:
        data = "DL"+phi_dots[0]+"R"+phi_dots[1]
        byte_data =bytearray()
        byte_data.extend(data)
        send_data = rospy.ServiceProxy(service_name, i2c_service)
        resp1 = send_data(True, byte_data,motor_interface_addr)
    except rospy.ServiceException, e:
       rospy.logwarn("Service call failed: %s",e)

try:
    listener()    
except rospy.ROSInterruptException as e:
    rospy.logerr("ROS-Error while runung %s : %s",node_name,str(e))

except Exception as e:
    rospy.logerr("uncaughed Error while running %s : Errorcode: %s",node_name,str(e))


