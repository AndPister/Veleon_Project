#!/usr/bin/env python

import rospy
from bike_services_pkg.srv import i2c_service
import smbus

server_node_name= 'i2c_service_server'
service_name='i2c_service'
bus_registration=1

def service_handler(req):

    if req.send_true:     
        send_data(req)
    else:
        read_data(req)
    return 

def send_data(req):
    bus.write_i2c_block_data(req.deviceID, 0x00,req.reqdata)

def read_data(req):
    response = bus.read_i2c_block_data(req.deviceID, 0x00)
    i2c_serviceRespons(response)
    
def main():
    rospy.init_node(server_node_name)
    s = rospy.Service(service_name,i2c_service,service_handler)
    rospy.spin()

if __name__=="__main__":
    try:
        main()
        bus = smbus.SMBus(bus_registration)
    except Exception as e:
        rospy.logerr(str(e))