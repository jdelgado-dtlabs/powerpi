# PowerPi
This project is for creating a power consumption monitor with Raspberry Pi. At the time of this writing, a Raspberry Pi 3 B+ was used. It is compatible with the Raspberry Pi 4.

Things you will need to install on your system:

1. Install Raspbian Buster with minimal options.
2. Install [InfluxDB](https://www.influxdata.com/blog/running-the-tick-stack-on-a-raspberry-pi/) using the latest repo version fron Influx themselves. **Do not use the version in Raspbian.**
3. Install [Grafana](https://grafana.com/grafana/download/6.3.0?platform=arm) using the latest repo version fron Influx themselves. **Do not use the version in Raspbian.**
4. Install Python3 and all the packages in the requirements.txt file.
5. Install Supervisord from the Raspbian repo. `sudo apt-get install supervisor`