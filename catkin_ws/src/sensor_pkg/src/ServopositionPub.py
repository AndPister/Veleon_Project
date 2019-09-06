#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
#Project:       Veleon-Project
#Subproject:    Low-Budget Sensors
#Autor:         Richard Bahmann
#Date:          01.09.19
#
#Discription: simple publisher that publishes into ServoPositio.
#                   10 to 170 degree only
#                     
#
#Input:         None
#                
#                   
#Output:      Servoposition in topic ServoPosition
#                   
#                   
#########################################################################

import rospy
from std_msgs.msg import Int16
Servoposition = 90


def ServopositionPubMAIN():
    rospy.init_node("ServopositionPub")
    publisher = rospy.Publisher("ServoPosition",Int16,queue_size=10)
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        publisher.publish(Servoposition)
        rate.sleep()






if __name__== "__main__":
        try:
            ServopositionPubMAIN()
        except rospy.ROSInterruptException:
            pass
