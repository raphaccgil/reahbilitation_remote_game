"""
A simple Python script to receive messages from a client over
Bluetooth using PyBluez (with Python 2).
"""

import socket, os
from src.util.fusion import Fusion
import re
import pandas as pd
import datetime

#UDP_IP = "192.168.1.101"
UDP_IP = ""
UDP_PORT = 2055

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)

print (sock)
sock.bind((UDP_IP, UDP_PORT))
count = 0
sep = Fusion()
a = []
list_variables = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
x_incr = 3
y_incr = 3
az = 0
ax = 0
stop_action = 0
acquir_data = Fusion()
'''
while ax <= 1000 or stop_action == 0:
    print 'read' + str(ax)
    ax += 1
    data, addr = sock.recvfrom(1024)
    date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz,  = re.split(',', data)
    mag = (float(magx), float(magy), float(magz))
    acquir_data.calibrate(mag, stop_action)
'''
while az <= 1000:

    data, addr = sock.recvfrom(1024)
    #print data
    date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz,  = re.split(',', data)
    gyrz = str(gyrz)
    gyrz = float(gyrz.replace("#", ""))

    acc = (float(accx), float(accy), float(accz))
    mag = (float(magx), float(magy), float(magz))
    gyr = (float(gyrx), float(gyry), float(gyrz))
    #if az == 0:
    date_val = datetime.datetime.fromtimestamp(float(date_time)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    print (date_val)
    if az == 0:
        print ('diff time == 0')
        acquir_data.update(acc, gyr, mag, 0)
    else:
        now_t = (date_time)
        diff = int(now_t) - int(last_t)
        diff *= 1000
        print ('diff time == {}'.format(str(diff)) )
        acquir_data.update(acc, gyr, mag, float(diff))
    last_t = date_time

    print ("Accx, Accy, Accz: {:7.3f} {:7.3f} {:7.3f}".format(float(accx), float(accy), float(accz)))
    print ("gyrx, gyry, gyrz: {:7.3f} {:7.3f} {:7.3f}".format(float(gyrx), float(gyry), float(gyrz)))
    print ("Heading, Pitch, Roll: {:7.3f} {:7.3f} {:7.3f}".format(acquir_data.heading, acquir_data.pitch, acquir_data.roll))

    list_variables[0].append(date_time)
    list_variables[1].append(accx)
    list_variables[2].append(accy)
    list_variables[3].append(accz)
    list_variables[4].append(magx)
    list_variables[5].append(magy)
    list_variables[6].append(magz)
    list_variables[7].append(gyrx)
    list_variables[8].append(gyry)
    list_variables[9].append(gyrz)
    list_variables[10].append(date_val)
    list_variables[11].append(acquir_data.heading)
    list_variables[12].append(acquir_data.pitch)
    list_variables[13].append(acquir_data.roll)
    #print data
    #print addr
    az += 1
    #last = datetime.datetime.now()

mag_var = pd.DataFrame(
    {'Datetime_unix': list_variables[0],
     'Datetime': list_variables[10],
     'Acceloremeter X': list_variables[1],
     'Acceloremeter Y': list_variables[2],
     'Acceloremeter Z': list_variables[3],
     'Mag X': list_variables[4],
     'Mag Y': list_variables[5],
     'Mag Z': list_variables[6],
     'Gyroscope X': list_variables[7],
     'Gyroscope Y': list_variables[8],
     'Gyroscope Z': list_variables[9],
     'Heading': list_variables[11],
     'Pitch': list_variables[12],
     'Roll': list_variables[13]
    })
path = 'C:\\Users\\Raphael\\Documents\\GitHub\\master_tel_remote\\presentation\\'
mag_var.to_csv(os.path.join(path, r'some_test.csv'), encoding='utf-8')




