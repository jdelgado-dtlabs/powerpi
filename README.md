# PowerPi
This project is for creating a power consumption monitor with Raspberry Pi. At the time of this writing, a Raspberry Pi 3 B+ was used. It is compatible with the Raspberry Pi 4.

Things you will need to install on your system:

1. Install Raspbian Buster with minimal options.
2. Install [InfluxDB](https://www.influxdata.com/blog/running-the-tick-stack-on-a-raspberry-pi/) using the latest repo version fron Influx themselves. **Do not use the version in Raspbian.**
3. Install [Grafana](https://grafana.com/grafana/download/6.3.0?platform=arm) using the latest version fron Grafana themselves. **Do not use the version in Raspbian.**
4. Install Python3 and all the packages in the requirements.txt file.
5. Install Supervisord from the Raspbian repo. `sudo apt-get install supervisor`

Hardware used:

1. [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
2. [Lechacal RPICT3V1](http://lechacal.com/wiki/index.php/RPICT3V1)
3. [SCT-013-000 Current Transformer 100A](https://www.amazon.com/CTYRZCH-SCT-013-000-Non-invasive-Current-Transformer/dp/B01C5JL5IY)
4. [US AC Adapter 77DA-10-09](http://lechacalshop.com/gb/internetofthing/54-usacac.html)
5. [5v 3A Power Adapter for RPi 3 with integrated switch](https://www.amazon.com/Yuconn-Charger-Adapter-Raspberry-SoundLink/dp/B071YC2T9S)

As a note, you don't need to install InfluxDB and Grafana on the same Raspberry Pi that you are reading energy data from. You can configure an external server that will accept your injested data. This can be a hosted solution as well as a on-premesis server. Just make the appropriate changes to `config.conf` with the proper `URL`, `Username` and `Password` of your external/hosted solution. Otherwise, it will all run from the Raspberry Pi just fine.