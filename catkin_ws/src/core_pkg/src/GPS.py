#!/usr/bin/env python

import serial
import pandas
import rospy
from std_msgs.msg import String

port = "/dev/ttyACM0"

print ("Receiving GPS data")
ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.5)

def parseGPSRMC(data):
	sdata = data.split(",")
	if sdata[2] =='V':
		print ("no sarellite data available")
		return
	print ("---Parsing GPRMC---")   
	time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
	lat = decode(sdata[3])	#latitude
	dirLat = sdata[4]		#latitude richtung N/S
	lon = decode(sdata[5])	#longitude
	dirLon = sdata[6]		#longitude richtung E/w
	speedknoten = sdata[7]		#Geschw in knots
	speedms = float(sdata[7])*0.5144	#Geschw in M/s	
	trCourse = sdata[8]		#True course
	date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]	#datum

	print ("time : %s, latitude : %s(%s), longitude : %s(%s), speedknoten : %s, speedms : %s, Troue Course : %s, Date : %s"%(time,lat,dirLat,lon,dirLon,speedknoten,speedms,trCourse,date))

def parseGPSGGA(data):
	ggadata = data.split(",")

    time = ggadata[1][0:2] + ":" + ggadata[1][2:4] + ":" + ggadata[1][4:6] + ggadata[1][7:8] #zeit utc mal auf sekunden achten
    lat = decode(ggadata[2])    #latitude
    dirLat = ggadata[3]         #latitude richtung N/S
    lon = decode(ggadata[4])    #longitude
    dirLong = ggadata[5]        #longitude richtung N/S
    if ggadata[6] == 0 : GPSqualit = ungueltig
    if ggadata[6] == 1 : GPSqualit = GPSfix
    if ggadata[6] == 2 : GPSqualit = DGPSfix
    if ggadata[6] == 6 : GPSqualit = geschaetzt
    usedSatellites = ggadata[7] #benutzte Satelliten max 12
    dilutop = ggadata[8]        #horizontale abweichung
    hnn = ggadata[9]            #hoehe d antenne ueber geoid
    hnnein = ggadata[10]        #einheit d antennenhoehe
    goisep = ggadata[11]        #geoidal seperation
    goisepein = ggadata[12]     #einheit geoidal sep
    Age = ggadata[13]           #alter des dgps datensatzes
    Refstatio = ggadata[14]     #dgps referenzstation

def decode(coord):
	#Konvertiert DDDMM.MMMMM zu DD deg MM.MMMMM min
	x = coord.split(".")
	head = x[0]
	tail = x[1]
	deg = head[0:-2]
	min = head[-2:]
	return (deg + "°" + min + "." + tail + "min")


def GPSMAIN ():

    pub     = rospy.Publisher#('string_publish', String, queue_size=10)
    
    rate    = rospy.Rate#(2)

    #msg_to_publish = String()

    while not rospy.is_shutdown():
	    data = ser.readline()
	    data = str(data)
        data = data[2:] #schneidet 'b am anfang ab
        if data[0:6] =="$GPRMC":
            parseGPSRMC(data)
        if data[0:6] =="$GPGGA":
            parseGPSGGA(data)

        #string_to_publish = "Publishing %d"
        #msg_to_publish.data = string_to_publish
        pub.publish(#msg_to_publish)
        rospy.loginfo(#string_to_publish)

        rate.sleep


if __name__== "__main__":
        try:
        ropy.init_node("GPS")
        GPSMAIN
    except rospy.ROSInterruptException:
        pass
    