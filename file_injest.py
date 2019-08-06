#!/usr/bin/python3

import configparser
import os, sys
import requests
import datetime
import time
import math
import signal

def termProcess(signalNumber, frame):
    print('Exiting...')
    sys.exit()

if __name__ =='__main__':
    signal.signal(signal.SIGINT, termProcess)

    c = configparser.ConfigParser()
    c.read("config.conf")

    f = open('testdata.txt', 'r')

    while True:
        
        data_in = f.readline()
        if not data_in:
            print('No more data or no data found')
            break

        utcnow = datetime.datetime.now()
		
        timestamp = utcnow.strftime("%s")
        #print(data_in)
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
        for dd in d[0:]:
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
        print(payload)
        r = requests.post(url, params=params, data=payload)
        print(r.text)
        time.sleep(2)