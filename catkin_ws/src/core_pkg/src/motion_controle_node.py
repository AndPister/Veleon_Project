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

enable_param = '/motion_controle/simulation_enable'
node_type_name = 'motion_controle_node'
wheel_pub_name = '/motion_controle/wheel_speed'
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
    if True: 
        phi_dot_r = (x_dot+d*alpha_dot)/R
        phi_dot_l = (x_dot-d*alpha_dot)/R
    else:
        #rospy.warn("Circle to small !! Default Values are used!! x_dot: %f alpha_dot:%f",%x_dot_default,%alpha_dot_default)
        phi_dot_r = 0
        phi_dot_l = 0


    return [phi_dot_l, phi_dot_r]

def listener():
    rospy.loginfo(R)
    rospy.loginfo("hallo")

    rospy.init_node(node_type_name,anonymous=True)
    rospy.Subscriber("/cmd_vel", Twist, calback)

    rospy.spin()
        
def calback(data):
        phi_dot = kinematics(data)
        rospy.loginfo(phi_dot)
        #phi_dot_pub = rospy.Publisher(wheel_pub_name,Float64MultiArray,queue_size=10)
        #phi_dot_pub.publish(phi_dot)


if __name__=="__main__":
        try:
            listener()    
        except Exception as e:
                rospy.logerr("Error while running core_info_node: " + str(e))


