#!/usr/bin/env python

import serial
import pandas
import rospy
from sensor_pkg.msg import GPSDATA_MSG

port = "/dev/ttyACM0"

print ("Receiving GPS data")
ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.5)

def parseGPSRMC(data):
	sdata = data.split(",")
	if sdata[2] =='V':
		print ("no sarellite data available")
		return
	print ("---Parsing GPRMC---")   
	timeRMC = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
	latRMC = decode(sdata[3])	#latitude
	dirLatRMC = sdata[4]		#latitude richtung N/S
	lonRMC = decode(sdata[5])	#longitude
	dirLonRMC = sdata[6]		#longitude richtung E/w
	speedknotenRMC = sdata[7]		#Geschw in knots
	speedmsRMC = float(sdata[7])*0.5144	#Geschw in M/s	
	trCourseRMCC = sdata[8]		#True course
	dateRMC = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]	#datum

    GPSMSG.latRMC = latRMC
    GPSMSG.dirLatRMC = dirLatRMC
    GPSMSG.lonRMC = lonRMC
    GPSMSG.dirLonRMC = dirLonRMC
    GPSMSG.speedmsRMC = speedmsRMC

	print ("time : %s, latitude : %s(%s), longitude : %s(%s), speedknoten : %s, speedms : %s, Troue Course : %s, Date : %s"%(timeRMC,latRMC,dirLatRMC,lonRMC,dirLonRMC,speedknotenRMC,speedmsRMC,trCourseRMC,dateRMC))

def parseGPSGGA(data):
	ggadata = data.split(",")

    timeGGA = ggadata[1][0:2] + ":" + ggadata[1][2:4] + ":" + ggadata[1][4:6] + ggadata[1][7:8] #zeit utc mal auf sekunden achten
    latGGA = decode(ggadata[2])    #latitude
    dirLatGGA = ggadata[3]         #latitude richtung N/S
    lonGGA = decode(ggadata[4])    #longitude
    dirLongGGA = ggadata[5]        #longitude richtung N/S
    if ggadata[6] == 0 : GPSqualitGGA = ungueltig
    if ggadata[6] == 1 : GPSqualitGGA = GPSfix
    if ggadata[6] == 2 : GPSqualitGGA = DGPSfix
    if ggadata[6] == 6 : GPSqualitGGA = geschaetzt
    usedSatellitesGGA = ggadata[7] #benutzte Satelliten max 12
    dilutopGGA = ggadata[8]        #horizontale abweichung
    hnnGGA = ggadata[9]            #hoehe d antenne ueber geoid
    hnneinGGA = ggadata[10]        #einheit d antennenhoehe
    goisepGGA = ggadata[11]        #geoidal seperation
    goisepeinGGA = ggadata[12]     #einheit geoidal sep
    AgeGGA = ggadata[13]           #alter des dgps datensatzes
    RefstatioGGA = ggadata[14]     #dgps referenzstation

    MSGGPS.latGGA = latGGA
    MSGGPS.dirLatGGA = dirLatGGA
    MSGGPS.lonGGA = lonGGA
    MSGGPS.dirLongGGA = dirLongGGA
    MSGGPS.GPSqualitGGA = GPSqualitGGA
    MSGGPS.usedSatellitesGGA = usedSatellitesGGA
    MSGGPS.hnnGGA = hnnGGA


def decode(coord):
	#Konvertiert DDDMM.MMMMM zu DD deg MM.MMMMM min
	x = coord.split(".")
	head = x[0]
	tail = x[1]
	deg = head[0:-2]
	min = head[-2:]
	return (deg + "°" + min + "." + tail + "min")


def GPSMAIN ():

    MSGGPS = GPSDATA_MSG()

    rospy.init_node("GPS")

    pub     = rospy.Publisher("GPSDATA", GPSDATA_MSG, queue_size=10)
    
    rate    = rospy.Rate(2)

    while not rospy.is_shutdown():
	    data = ser.readline()
	    data = str(data)
        data = data[2:] #schneidet 'b am anfang ab
        if data[0:6] =="$GPRMC":
            parseGPSRMC(data)
        if data[0:6] =="$GPGGA":
            parseGPSGGA(data)

        pub.publish(MSGGPS)

        rate.sleep()


if __name__== "__main__":
        try:
        GPSMAIN()
    except rospy.ROSInterruptException:
        pass
    