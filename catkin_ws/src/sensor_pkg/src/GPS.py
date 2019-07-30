#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import pandas
import rospy
from sensor_pkg.msg import GPSDATA_MSG

serialport = "/dev/ttyACM0"
nodename = "GPS"
topic = "GPSDATA"
sensorrate = 2


def parseGPSRMC(data):
    sdata = data.split(",")
    if sdata[2] =='V':
        print ("no satellite data available") #entsprechend bei error message ergaenzen
        return
    print ("---Parsing GPRMC---")   
    timeRMC = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
    latRMC = decode(sdata[3])	#latitude
    dirLatRMC = sdata[4]		#latitude richtung N/S
    lonRMC = decode(sdata[5])	#longitude
    dirLonRMC = sdata[6]		#longitude richtung E/w
    speedknotenRMC = sdata[7]		#Geschw in knots
    speedmsRMC = float(sdata[7])*0.5144	#Geschw in M/s	
    trCourseRMC = sdata[8]		#True course
    dateRMC = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]	#datum


    #print ("time : %s, latitude : %s(%s), longitude : %s(%s), speedknoten : %s, speedms : %s, Troue Course : %s, Date : %s"%(timeRMC,latRMC,dirLatRMC,lonRMC,dirLonRMC,speedknotenRMC,speedmsRMC,trCourseRMC,dateRMC))
    return True,latRMC,dirLatRMC,lonRMC,dirLonRMC,speedmsRMC

def parseGPSGGA(data):
        ggadata = data.split(",")
        
        print ("---Parsing GPGGA---")
        timeGGA = ggadata[1][0:2] + ":" + ggadata[1][2:4] + ":" + ggadata[1][4:6] + ggadata[1][7:8] #zeit utc mal auf sekunden achten
        latGGA = decode(ggadata[2])    #latitude
        dirLatGGA = ggadata[3]         #latitude richtung N/S
        lonGGA = decode(ggadata[4])    #longitude
        dirLonGGA = ggadata[5]        #longitude richtung N/S
        if ggadata[6] == 1 : GPSqualityGGA = 'GPSfix'
        elif ggadata[6] == 2 : GPSqualityGGA = 'DGPSfix'
        elif ggadata[6] == 6 : GPSqualityGGA = 'estimate'
        else  : GPSqualityGGA = 'invalid'
        usedSatellitesGGA = ggadata[7] #benutzte Satelliten max 12
        dilutopGGA = ggadata[8]        #horizontale abweichung
        hnnGGA = ggadata[9]            #hoehe d antenne ueber geoid
        hnneinGGA = ggadata[10]        #einheit d antennenhoehe
        goisepGGA = ggadata[11]        #geoidal seperation
        goisepeinGGA = ggadata[12]     #einheit geoidal sep
        AgeGGA = ggadata[13]           #alter des dgps datensatzes
        RefstatioGGA = ggadata[14]     #dgps referenzstation
        
        return True,latGGA,dirLatGGA,lonGGA,dirLonGGA,GPSqualityGGA,hnnGGA

def decode(coord):
        #Konvertiert DDDMM.MMMMM zu DD deg MM.MMMMM min
        x = coord.split(".")
        head = x[0]
        tail = x[1]
        deg = head[0:-2]
        min = head[-2:]
        return (deg + "." + min + "." + tail + "min")


def GPSMAIN ():

    print ("Receiving GPS data")
    ser = serial.Serial(serialport, baudrate = 9600, timeout = 0.5)

    

    rospy.init_node(nodename)

    publisher     = rospy.Publisher(topic, GPSDATA_MSG, queue_size=10)
    
    rate    = rospy.Rate(sensorrate)

    while not rospy.is_shutdown():
        MSGGPS = GPSDATA_MSG()
        jump_out_R=False
        jump_out_G=False
        while not jump_out_R or not jump_out_G:
            data = ser.readline()
            data = str(data)
        
            #data = data[1:]         #schneidet 'b am anfang ab
            print(data)
            #if "$GPRMC" in data:
            if data[0:6] =="$GPRMC":
                jump_out_R,latRMC,dirLatRMC,lonRMC,dirLonRMC,speedmsRMC=parseGPSRMC(data)
                MSGGPS.latRMC = latRMC
                MSGGPS.dirLatRMC = dirLatRMC
                MSGGPS.lonRMC = lonRMC
                MSGGPS.dirLonRMC = dirLonRMC
                MSGGPS.speedmsRMC = speedmsRMC
            if data[0:6] =="$GPGGA":
                jump_out_G,latGGA,dirLatGGA,lonGGA,dirLonGGA,GPSqualityGGA,hnnGGA=parseGPSGGA(data)  
                MSGGPS.latGGA = latGGA
                MSGGPS.dirLatGGA = dirLatGGA
                MSGGPS.lonGGA = lonGGA
                MSGGPS.dirLonGGA = dirLonGGA
                MSGGPS.GPSqualityGGA = GPSqualityGGA
                MSGGPS.hnnGGA = hnnGGA
            #else gpsdatenfehler ueber variable ausgeben => ueber GPSDATA publishen "couldnt find gpsdata"
        publisher.publish(MSGGPS)

        rate.sleep()


if __name__== "__main__":
    try:
        GPSMAIN()
    except rospy.ROSInterruptException:
        pass
    
