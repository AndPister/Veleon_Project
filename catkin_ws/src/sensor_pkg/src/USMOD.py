#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_pkg.msg import USMOD_MSG
#from bike_service_pkg.srv import i2c_service

adress_nano_1 = 0x10a
adress_nano_2 = 0x11a
USMODDATA = USMOD_MSG()

def USMODMAIN():

    rospy.init_node("USMOD")
    rate = rospy.Rate(20)
    rospy.wait_for_service('i2c_service')
    trigger1 = rospy.ServiceProx('i2c_service',i2c_service)
    trigger2 = rospy.ServiceProx('i2c_service',i2c_service)

    pub = rospy.Publisher("USMODDATA", USMOD_MSG)

    while not rospy.is_shutdown():

        trigger1(TRUE,0,adress_nano_1)
        return trigger1.resdata
        USMODDATA.Sensordaten1 = trigger1.resdata
        trigger2(TRUE,0,adress_nano_2)
        return trigger2.resdata
        USMODDATA.Sesnordaten2 = trigger2.resdata

        pub.publish(USMODDATA)


        rate.sleep()




if __name__== "__main__":
        try:
        USMODMAIN()
    except rospy.ROSInterruptException:
        pass
    