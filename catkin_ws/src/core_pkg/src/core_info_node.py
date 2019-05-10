#!/usr/bin/env python
import rospy
import psutil
from std_msgs.msg import Float32



def core_info(pub_core,pup_mem,spintime):
#Publish core infos
#CPU-usage RAM-usage
        rate = rospy.rate(spintime)
        core_usage = psutil.cpu_percent()
        rospy.loginfo(core_usage)
        pub.publish(core_usage)

def check_core_release()
        return True

def main():
        pub_core = rospy.Publisher('/core_info_node/core_usage', Float32, queue_size=10)
        pub_memory= rospy.Publisher('/core_info_node/core_usage', Float32, queue_size=10)
        rospy.init_node('core_info_node', anonymous=True)
        while not rospy.is_shutdown():
                if check_core_release():
                        core_info(pub_core=pub_core,pub_memory=pub_memory,10)
                

if __name__=="__main__":
        try:
                main()
        except:
                rospy.loginfo("Error while running core_info_node")

