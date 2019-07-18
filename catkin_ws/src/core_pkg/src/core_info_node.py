#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#Project: Veleon-Project
#Subproject: Publish Coreinformation for performancecheck
#Autor: Andreas Pister
#Date:10.05.19
#####################################################################



import rospy
import psutil
from std_msgs.msg import Float32

enable_param = '/core_info/core_info_enable'
node_type_name = 'core_info_node'
core_pub_name = '/core_info/core_usage'

def core_info(pub_core,pub_mem,spintime):
#Publish core infos
#CPU-usage
        rate = rospy.Rate(spintime)
        core_usage = psutil.cpu_percent()
        memory = psutil.swap_memory()
        ram_usage = memory
        rospy.loginfo("Core-usage: " + str(core_usage))
        pub_core.publish(core_usage)
        #pub_mem.publish(ram_usage)
        rate.sleep()

def check_core_release():
        enable = rospy.get_param(enable_param)
        if enable is None:
                raise Exception ("No Param : "+enable_param+" found")
        return enable

def main():
        pub_core = rospy.Publisher(core_pub_name, Float32, queue_size=10)
        
        pub_memory =None
        rospy.init_node(node_type_name, anonymous=True)
        while not rospy.is_shutdown():
                if check_core_release():
                        core_info(pub_core=pub_core,pub_mem=pub_memory,spintime=5)
                

if __name__=="__main__":
        try:
                if rospy.has_param(enable_param):
                        main()
                else:
                        rospy.loginfo("Param: core_info_enable not found ")
        except Exception as e:
                rospy.loginfo("Error while running core_info_node: " + str(e))


