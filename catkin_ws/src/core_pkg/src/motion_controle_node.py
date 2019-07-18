#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

service_name ='i2c_sevice'
spinningrate= 10

adress_motor_left = 0x2a
adress_motor_right =0x3a

x_dot_default = 0.0
alpha_dot_default = 0.0
accuracy= 3

beschleunigungsrampe = 0.5
verzögerungsrampe = 0.5
phi_dot_alt= [0.000,0.000] # [links,rechts]
R = 0.503         
d = 0.77/2
class generate_ramp():  
    def generate_ramp(self,phi_dot,phi_dot_alt):
        self.phi_dot =phi_dot
        self.phi_dot_alt = phi_dot_alt
        if self.phi_dot = phi_dot_alt:
            return self.phi_dot
        elif self.phi_dot < 0 and self.phi_dot_alt < 0:
            self.phi_dot*= -1
            self.phi_dot_alt*= -1
            return beschleunigung()*-1
        elif self.phi_dot> self.phi_dot_alt:
            return beschleunigung() 
        elif self.phi_dot < self.phi_dot_alt:
            return verzögerung()

    def beschleunigung(self,sign):
        phi_dot_output = self.phi_dot_alt + beschleunigungsrampe*(1/spinningrate)
        if self.phi_dot < phi_dot_output:
            phi_dot_output = self.phi_dot
        return phi_dot_output

    def verzögerung(self):
        phi_dot_output = self.phi_dot_alt - verzögerungsrampe*(1/spinningrate)
        if self.phi_dot < phi_dot_output:
            phi_dot_output = self.phi_dot
        return phi_dot_output 


def kinematics(cmd_vel):
    '''
    This Funktion includes the kinematic mathematics.
    Input: cmd_vel-content
    Output: phi_dot
    '''
    x_dot = cmd_vel.linear.x
    alpha_dot = cmd_vel.angular.z 
    rampe= generate_ramp()

    #check if join-angle is in Tolerance
    if rospy.get_param('/emergancy_stopp',False): 
        phi_dot_r = (x_dot+d*alpha_dot)/R
        phi_dot_l = (x_dot-d*alpha_dot)/R
        phi_dot_r = rampe.generate_ramp(phi_dot_r,phi_dot_alt[1])
        phi_dot_l = rampe.generate_ramp(phi_dot_l,phi_dot_alt[0])
        phi_dot_alt=[phi_dot_l,phi_dot_r]
    elif rospy.get_param('/emergancy_stopp'):
        rospy.logerr("Emergency stop is active ")
        phi_dot_r = 'F'
        phi_dot_l = 'F'
    elif rospy.get_param('/stopp',False):
        phi_dot_r = rampe.generate_ramp(0.0,phi_dot_alt[1])
        phi_dot_l = rampe.generate_ramp(0.0,phi_dot_alt[0])
        phi_dot_alt=[phi_dot_l,phi_dot_r]
    else:
        rospy.logerr("Circle to small !! Default Values are used!! x_dot: %s alpha_dot:%s",x_dot_default,alpha_dot_default)
        phi_dot_r = 0.0
        phi_dot_l = 0.0
    return [phi_dot_l, phi_dot_r]

def listener():
    rospy.init_node(node_name,anonymous=False)
    topic_name ='/tele_op'
    rospy.logdebug("Used Topic: %s", topic_name)
    rate = rospy.Rate(spinningrate)
    while not rospy.is_shutdown():
        topic_name = check_topic(topic_name)
        rospy.Subscriber(topic_name, Twist, calback)
        rate.sleep()

def send_value(phi_dot,address):
    rospy.wait_for_service(service_name)
    try:
        send_data = rospy.ServiceProxy(service_name,i2c_sevice)
        if type(phi_dot)==float:
            send_data(True, address,bytearray().extend(round(phi_dot,accuracy)))
        else:
            send_data(True, address,bytearray().extend(phi_dot))
    except rospy.ServiceException as e:
        rospy.logwarn("Service_call faild: %s",e)

def calback(data):
    phi_dot = kinematics(data)
    send_value(phi_dot[0],adress_motor_left)
    send_value(phi_dot[1],adress_motor_right)
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


