#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_pkg.msg import USMOD_MSG
from bike_services_pkg.srv import i2c_service

adress_nano_1 = 0x3a
adress_nano_2 = 0x4a
nodename = "USMOD"
topic = "USMODDATA"


def USMODMAIN():

    rospy.init_node(nodename)
    rate = rospy.Rate(20)
    rospy.wait_for_service('i2c_service')
    trigger1 = rospy.ServiceProxy('i2c_service',i2c_service)
    trigger2 = rospy.ServiceProxy('i2c_service',i2c_service)

    publisher = rospy.Publisher(topic, USMOD_MSG,queue_size=10)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        USMODDATA = USMOD_MSG()
        rospy.wait_for_service('i2c_service')
        antwort = trigger1(False,adress_nano_1,bytearray())
        antwort1 = antwort.resdata
        ant=antwort1[0:4]
        print(type(ant))
        print(ant)
        
        USMODDATA.Sensordaten1 = ant
        antwort2 = trigger2(False,adress_nano_2,bytearray(0))
        antwort2 = antwort2.resdata
        ant2=antwort2[0:4]
        print(ant2)

        USMODDATA.Sensordaten2 = ant2
        publisher.publish(USMODDATA)


        rate.sleep()


#i2c_service SERVER muss noch antworten koennen. muss hinyugefuegt werrden !!!!!11
#prolly return i2c_serviceResponse


if __name__== "__main__":
    try:
        USMODMAIN()
    except rospy.ROSInterruptException:
        pass
    
