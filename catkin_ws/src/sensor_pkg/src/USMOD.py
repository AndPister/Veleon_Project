#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
#Project:       Veleon-Project
#Subproject:    Low-Budget Sensors
#Autor:         Richard Bahmann
#Date:          01.08.19
#
#Discription:   Node covers the reading of the ultrasonic sensors of the Veleon-Bike.
#                     It also transform the coordinates relative to the module center point
#                     uses I2C
#
#Input:         None
#                
#                   
#Output:        Ultrasonic data in both forms: transforme and not transformed in USMODDATA
#                   
#                   
#########################################################################

import rospy
import math
from sensor_pkg.msg import USMOD_MSG
from bike_services_pkg.srv import i2c_service
import time

adress_nano_1 = 0x3a
adress_nano_2 = 0x4a
adress_nano_3 = 0x5a
nodename = "USMOD"
topic = "USMODDATA"

Sin_6_degree = (math.sin(6*math.pi/180))
Cos_6_degree = (math.cos(6*math.pi/180))

#Transformation of the coord is set to the acrylic glass exponator and has to be adjusted to the constructed housing, if ever printed.
#degree can easily be changed above. recommended to add needed degrees like above for easier use.
#Data comes like this:
#       ____________________________________
#       |    2   |    3   |               |    6   |    7   |
#       |    1   |    4   |               |    5   |    8   |
#
#       ant      (7|8|6|5)
#       ant2    (3|4|2|1)


def Koordtransformback1(Koord):
    Measurement1 = [Cos_6_degree*Koord[3]-0.455,Sin_6_degree*-1*Koord[3]-14.68,Sin_6_degree*-1*Koord[3]-5.989] 
    Measurement2 = [Cos_6_degree*Koord[2]-0.365,Sin_6_degree*-1*Koord[2]-14.68,-2.0]
    Measurement3 = [Koord[0],-7.7,-2.0]
    Measurement4 = [Cos_6_degree*Koord[1]-0.209,-7.7,Sin_6_degree*Koord[1]-5.989]
    return Measurement1,Measurement2,Measurement3,Measurement4
def Koordtransformback2(Koord2):
    Measurement5 = [Cos_6_degree*Koord2[3]-0.209,7.7,Sin_6_degree*Koord2[3]-5.989]
    Measurement6 = [Koord2[2],7.7,-2.0]
    Measurement7 = [Cos_6_degree*Koord2[0]-0.365,Sin_6_degree*-1*Koord2[0]+14.68,-2.0] 
    Measurement8 = [Cos_6_degree*Koord2[1]-0.455,Sin_6_degree*Koord2[1]+14.68,Sin_6_degree*-1*Koord2[1]-5.989] 
    return Measurement5,Measurement6,Measurement7,Measurement8
def Koordtransformfront(Koord3):
    Measurement_front_left = [Koord3[0],-15,0]
    Measurement_front_right = [Koord3[1],15,0]
    return Measurement_front_left,Measurement_front_right


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
            #print(type(ant))
            print(ant)
            
            M5,M6,M7,M8=Koordtransformback2(ant)
            #print("5-8")
            #print(M5)
            #print(M6)
            #print(M7)
            #print(M8)
            
            USMODDATA.Measurement5 = M5
            USMODDATA.Measurement6 = M6
            USMODDATA.Measurement7 = M7
            USMODDATA.Measurement8 = M8
            USMODDATA.Sensordaten1 = ant
        except rospy.ServiceException as e:
            rospy.logwarn("Service_call failed: %s",e)

        rospy.wait_for_service('i2c_service')
        time.sleep(0.5)
        try:
            antwort2 = trigger2(False,adress_nano_2,bytearray(0))
            antwort2 = antwort2.resdata
            ant2=antwort2[0:4]
            
            M1,M2,M3,M4=Koordtransformback1(ant2)
            #print("1-4")
            #print(M1)
            #print(M2)
            #print(M3)
            #print(M4)
            print(ant2)
            USMODDATA.Measurement1 = M1
            USMODDATA.Measurement2 = M2
            USMODDATA.Measurement3 = M3
            USMODDATA.Measurement4 = M4
            USMODDATA.Sensordaten2 = ant2
        except rospy.ServiceException as e:
            rospy.logwarn("Service_call failed: %s",e)
        rospy.wait_for_service('i2c_service')
        try:
            antwort3 = trigger3(False,adress_nano_3,bytearray(0))
            antwort3 = antwort3.resdata
            ant3=antwort3[0:2]

            Mfr,Mfl=Koordtransformfront(ant3)

            #print("front")
            #print(Mfr)
            #print(Mfl)
            
            print(ant3)
            USMODDATA.SensordatenVorne = ant3
        except rospy.ServiceException as e:
            rospy.logwarn("Service_call failed: %s",e)
            


        publisher.publish(USMODDATA)


        rate.sleep()



if __name__== "__main__":
    try:
        USMODMAIN()
    except rospy.ROSInterruptException:
        pass
    
