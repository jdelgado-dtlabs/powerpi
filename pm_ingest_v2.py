#!/usr/bin/python3

from configparser import ConfigParser
from serial import Serial
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os, sys
import requests
import datetime
import math
import signal

def printStatus(message):
    dt = datetime.datetime.now()
    d = dt.strftime("%Y-%m-%d %H:%M:%S")
    for m in message.splitlines():
        print(f"[{d}] {m}")

def termProcess(signalNumber, frame):
    printStatus('Exiting...')
    sys.exit()

def pull_serial_data(serial):
    try:
        serial.open()
    except:
        pass
    data_in = serial.readline()
    serial.close()
    if not data_in:
        printStatus('No data received')
        return False

    data_in = data_in.decode("utf-8")
    while data_in[-1] in ['\r', '\n']:
        data_in = data_in[:-1]
    try:
        return data_in.split(' ')
    except:
        printStatus("Bad data. Skipping.")
        return False

def generate_payload(dataset, device):
    i = 0
    payload = []
    for data in dataset[1:]:
        i += 1
        if i == 1 or i == 6 or i == 11:
            channel = math.ceil(i/5)
            payload.append(f"realpower,device={device},channel=0{channel} value={data}")
        if i == 2 or i == 7 or i == 12:
            channel = math.ceil(i/5)
            payload.append(f"apparantpower,device={device},channel=0{channel} value={data}")
        if i == 3 or i == 8 or i == 13:
            channel = math.ceil(i/5)
            payload.append(f"irms,device={device},channel=0{channel} value={data}")
        if i == 4 or i == 9 or i == 14:
            channel = math.ceil(i/5)
            payload.append(f"vrms,device={device},channel=0{channel} value={data}")
        if i == 5 or i == 10 or i == 15:
            channel = math.ceil(i/5)
            payload.append(f"powerfactor,device={device},channel=0{channel} value={data}")
        else:
            return payload

if __name__ =='__main__':
    signal.signal(signal.SIGINT, termProcess)

    c = ConfigParser()
    c.read("config.conf")

    baud = c.getint('system','baud')
    serial_port = c.get('system', 'port')
    url = c.get('influxdb', 'url')
    bucket = c.get('influxdb', 'bucket')
    token = c.get('influxdb', 'token')
    org = c.get('influxdb', 'org')
    device = c.get('influxdb', 'device')
    if not os.path.exists(serial_port):
        printStatus('Serial port not found')
        sys.exit()

    while True:
        dataset = pull_serial_data(Serial(serial_port, baud, timeout=3))
        if dataset:
            payload = generate_payload(dataset, device)
            with InfluxDBClient(url=url, token=token, org=org) as client:
                write_api = client.write_api(write_options=SYNCHRONOUS)
                write_api.write(bucket, org, payload)
            client.close()
                