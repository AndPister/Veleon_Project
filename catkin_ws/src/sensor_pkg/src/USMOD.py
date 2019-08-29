#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_pkg.msg import USMOD_MSG
from bike_services_pkg.srv import i2c_service
import time

adress_nano_1 = 0x3a
adress_nano_2 = 0x4a
adress_nano_3 = 0x5a
nodename = "USMOD"
topic = "USMODDATA"


def USMODMAIN():

    rospy.init_node(nodename)
    rospy.wait_for_service('i2c_service')
    trigger1 = rospy.ServiceProxy('i2c_service',i2c_service)
    trigger2 = rospy.ServiceProxy('i2c_service',i2c_service)
    trigger3 = rospy.ServiceProxy('i2c_service',i2c_service)

    publisher = rospy.Publisher(topic, USMOD_MSG,queue_size=10)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        USMODDATA = USMOD_MSG()
        try:
            rospy.wait_for_service('i2c_service')
            antwort = trigger1(False,adress_nano_1,bytearray(0))
            antwort1 = antwort.resdata
            ant=antwort1[0:4]
            print(type(ant))
            print(ant)
            USMODDATA.Sensordaten1 = ant
        except rospy.ServiceException as e:
            rospy.logwarn("Service_call failed: %s",e)

        rospy.wait_for_service('i2c_service')
        time.sleep(0.5)
        try:
            antwort2 = trigger2(False,adress_nano_2,bytearray(0))
            antwort2 = antwort2.resdata
            ant2=antwort2[0:4]
            print(ant2)
            USMODDATA.Sensordaten2 = ant2
        except rospy.ServiceException as e:
            rospy.logwarn("Service_call failed: %s",e)
        rospy.wait_for_service('i2c_service')
        try:
            antwort3 = trigger3(False,adress_nano_3,bytearray(0))
            antwort3 = antwort3.resdata
            ant3=antwort3[0:2]
            print(ant3)
            USMODDATA.SensordatenVorne = ant3
        except rospy.ServiceException as e:
            rospy.logwarn("Service_call failed: %s",e)
            


        publisher.publish(USMODDATA)


        rate.sleep()


#i2c_service SERVER muss noch antworten koennen. muss hinyugefuegt werrden !!!!!11
#prolly return i2c_serviceResponse


if __name__== "__main__":
    try:
        USMODMAIN()
    except rospy.ROSInterruptException:
        pass
    
