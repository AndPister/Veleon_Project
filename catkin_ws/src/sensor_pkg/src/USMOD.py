#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_pkg.msg import USMOD_MSG
from bike_service_pkg.srv import i2c_service

adress_nano_1 = 0x10a
adress_nano_2 = 0x11a
nodename = "USMOD"
topic = "USMODDATA"


def USMODMAIN():

    rospy.init_node(nodename)
    rate = rospy.Rate(20)
    rospy.wait_for_service('i2c_service')
    trigger1 = rospy.ServiceProx('i2c_service',i2c_service)
    trigger2 = rospy.ServiceProx('i2c_service',i2c_service)

    publisher = rospy.Publisher(topic, USMOD_MSG)

    while not rospy.is_shutdown():
        USMODDATA = USMOD_MSG()
        trigger1(FALSE,adress_nano_1)
        return trigger1.resdata
        USMODDATA.Sensordaten1 = trigger1.resdata
        trigger2(FALSE,adress_nano_2)
        return trigger2.resdata
        USMODDATA.Sesnordaten2 = trigger2.resdata

        publisher.publish(USMODDATA)


        rate.sleep()


#i2c_service SERVER muss noch antworten koennen. muss hinyugefuegt werrden !!!!!11
#prolly return i2c_serviceResponse


if __name__== "__main__":
        try:
        USMODMAIN()
    except rospy.ROSInterruptException:
        pass
    