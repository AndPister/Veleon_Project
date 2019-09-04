#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import struct
from std_msgs.msg import Int16
from bike_services_pkg.srv import i2c_service

adress_nano_3 = 0x5a
nodename = "FRONTMOD"

def callback(data):
    Servopos = data.data
    #print(Servopos)
    setservo(Servopos)
    

def setservo(Servopos):
    rospy.wait_for_service('i2c_service')
    try:
        send_value = rospy.ServiceProxy('i2c_service',i2c_service)
        if(Servopos >= 10 and Servopos <=170):
            pos_data=[i for i in bytearray(struct.pack("i",Servopos))]
            print(type(pos_data))
            print(pos_data)
            send_value(True,adress_nano_3, pos_data)
            print("gesendet")
        else:
            rospy.logwarn("Value for servo has to be between 0 and 180")
    except rospy.ServiceException as e:
        rospy.logwarn("Service_call failed: %s",e)

def FRONTMODMAIN():

    rospy.init_node(nodename)
    #trigger3 = rospy.ServiceProx('i2c_service',i2c_service)


    rospy.Subscriber("ServoPosition",Int16,callback)
    rospy.spin()




if __name__== "__main__":
        try:
            FRONTMODMAIN()
        except rospy.ROSInterruptException:
            pass
