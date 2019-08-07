#!/usr/bin/python3

import configparser
import serial
import os, sys
import requests
import datetime
import math
import signal

def printStatus(message):
    dt = datetime.datetime.now()
    d = dt.strftime("%Y-%m-%d %H:%M")
    for m in message.splitlines():
        print("[%s] %s" % (d, m))

def termProcess(signalNumber, frame):
    printStatus('Exiting...')
    sys.exit()

if __name__ =='__main__':
    signal.signal(signal.SIGINT, termProcess)

    c = configparser.ConfigParser()
    c.read("config.conf")

    baud = c.getint('system','baud')
    serial_port = c.get('system', 'port')
    if not os.path.exists(serial_port):
        printStatus('Serial port not found')
        sys.exit()
    ser = serial.Serial(serial_port, baud, timeout=3)

    while True:
        try:
            ser.open()
        except:
            pass
        data_in = ser.readline()
        ser.close()
        if not data_in:
            printStatus('No data received')
            continue

        utcnow = datetime.datetime.now()
		
        timestamp = utcnow.strftime("%s")
        #printStatus(data_in)
        while data_in[-1] in ['\r', '\n']:
            data_in = data_in[:-1]

        d = data_in.split(' ')
        t = timestamp + '000000000'
        url = c.get('influxdb', 'url')
        dbname = c.get('influxdb', 'dbname')
        user = c.get('influxdb', 'user')
        passwd = c.get('influxdb', 'passwd')
        device = c.get('influxdb', 'device')
        if user and passwd:
            params = {'db': dbname, 'u': user, 'p': passwd}
        else:
            params = {'db': dbname}

        i = 0
        payload = ""
        for dd in d[1:]:
            i += 1
            if i == 1 or i == 6 or i == 11:
                nn = math.ceil(i/5)
                payload += "realpower,device=%s,channel=%02d value=%s %s\n" % (device, nn, dd, t)
            if i == 2 or i == 7 or i == 12:
                nn = math.ceil(i/5)
                payload += "apparantpower,device=%s,channel=%02d value=%s %s\n" % (device, nn, dd, t)
            if i == 3 or i == 8 or i == 13:
                nn = math.ceil(i/5)
                payload += "irms,device=%s,channel=%02d value=%s %s\n" % (device, nn, dd, t)
            if i == 4 or i == 9 or i == 14:
                nn = math.ceil(i/5)
                payload += "vrms,device=%s,channel=%02d value=%s %s\n" % (device, nn, dd, t)
            if i == 5 or i == 10 or i == 15:
                nn = math.ceil(i/5)
                payload += "powerfactor,device=%s,channel=%02d value=%s %s\n" % (device, nn, dd, t)
            else:
                pass

        #payload = "rpict3t1,channel=01 value=50.2 %s\nrpict3t1,channel=02 value=156.2 %s\n" % (t,t)
        printStatus(payload)
        r = requests.post(url, params=params, data=payload)
        printStatus(r.text)