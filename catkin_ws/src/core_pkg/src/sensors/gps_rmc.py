#!/usr/bin/env python3

import serial

port = "/dev/ttyACM0"

def parseGPS(data):
    if data[0:6] =="$GPRMC":
        sdata = data.split(",")
        if sdata[2] =='V':
            print ("no satellite data available")
            return
        print ("---Parsing GPRMC---")   
        time = sdata[1][0:2]  ":"  sdata[1][2:4]  ":" sdata[1][4:6]
        lat = decode(sdata[3])  #latitude
        dirLat = sdata[4]       #latitude richtung N/S
        lon = decode(sdata[5])  #longitude
        dirLon = sdata[6]       #longitude richtung E/w
        speed = sdata[7]        #Geschw in knots
        trCourse = sdata[8]     #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] #datum

        print ("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, Troue Course : %s, Date : %s" % (time,lat,dirLat,lon,dirLon,soeed,trCourse,date))

def decode(coord):
    #Konvertiert DDDMM.MMMMM zu DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return (deg + "deg" + min + "." + tail + "min")

print ("Receiving GPS data")
ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.5)
while True:
    data = ser.readline()
    parseGPS(data)