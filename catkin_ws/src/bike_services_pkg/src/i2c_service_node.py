#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from bike_services_pkg.srv import i2c_service, i2c_serviceResponse
import smbus
import time

server_node_name= 'i2c_service_server'
service_name='i2c_service'
bus_registration=1
cmd =10


bus = smbus.SMBus(bus_registration)
time.sleep(1) #wait here to avoid error121

def service_handler(req):
    
    if req.send_true:     
        send_data(req)
    else:
        res=read_data(req)
        print(res)
        return i2c_serviceResponse(res)
    return 

def send_data(req):
    print("sende")
    test=[i for i in bytearray(req.reqdata)]
    bus.write_i2c_block_data(req.deviceID, cmd,test)
    return 

def read_data(req):
    print("empfaengt")
    response = bus.read_i2c_block_data(req.deviceID, cmd)
    print(type(response))
    return response
    
def main():
    print("startet")
    rospy.init_node(server_node_name)
    s = rospy.Service(service_name,i2c_service,service_handler)
    rospy.spin()

try:
    main()
except Exception as e:
    rospy.logerr(str(e))
