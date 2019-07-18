#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from bike_services_pkg.srv import i2c_service
import smbus

server_node_name= 'i2c_service_server'
service_name='i2c_service'
bus_registration=1
cmd =0x0a


bus = smbus.SMBus(bus_registration)

def service_handler(req):
    rate= rospy.Rate(10)
    if req.send_true:     
        send_data(req)
    else:
        read_data(req)
    
    rate.sleep()
    return 

def send_data(req):
    bus.write_i2c_block_data(req.deviceID, cmd,req.reqdata)
    return 

def read_data(req):
    response = bus.read_i2c_block_data(req.deviceID, cmd)
    return response
    
def main():
    rospy.init_node(server_node_name)
    s = rospy.Service(service_name,i2c_service,service_handler)
    rospy.spin()

try:
    main()
except Exception as e:
    rospy.logerr(str(e))