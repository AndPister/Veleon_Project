#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import Int16
#from bike_service_pkg.srv import i2c_service

adress_nano_3 = 0x20a

def callback(data):
    SERVODATA = data

def FRONTMODMAIN():

    rospy.init_node("USMOD")
    rate = rospy.Rate(20)
    rospy.wait_for_service('i2c_service')
    trigger3 = rospy.ServiceProx('i2c_service',i2c_service)

    pub = rospy.Publisher("FRONTMODDATA", Int64MultiArray)

    rospy.Subscriber("SERVODATA",Int16,callback)

    while not rospy.is_shutdown():

        trigger3(TRUE,SERVODATA,adress_nano_3)
        return trigger3.resdata
        pub.publish(trigger3.resdata)




        rate.sleep()







if __name__== "__main__":
        try:
        FRONTMODMAIN()
    except rospy.ROSInterruptException:
        pass