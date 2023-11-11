# Introduction to IoT-Based Systems - Project

## Introduction 

This code repository contains all scripts used in the LUT course project of BL40A2010 Introduction to IoT-Based Systems. This readme file acts as a tutorial to replicate the system we have used.

## Database

This project requires an instance of InfluxDB Cloud Serverless. We have subscribed to the InfluxDB Cloud Serverless Free Plan through InfluxData [here](https://cloud2.influxdata.com/signup). Instructions for signing up can be found [here](https://docs.influxdata.com/influxdb/cloud-serverless/sign-up/#sign-up). 

- After creating an account, create a bucket called environment using the web interface.
- Create an all access API token using the web interface and save it for later use.

## Sensor system

To setup the sensor emulation environment, create a Linux Ubuntu virtual machine. We have created it as follows:

- [Download & install Oracle VM VirtualBox](https://www.virtualbox.org/)
- Download the [latest LTS version of Linux Ubuntu](https://ubuntu.com/download/desktop)
- Create a Linux Ubuntu virtual machine
- Install the [Sense HAT emulator software](https://www.raspberrypi.org/blog/desktop-sense-hat-emulator/) using terminal:

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-sense-emu sense-emu-tools
```

- After installing the Sense HAT emulator and the Python 3 library, open the Sense HAT emulator with

```bash
sense_emu_gui
```

- To send example measurements to the InfluxDB database you previously set up, run the measure.py script.

```bash
export INFLUXDB_TOKEN="<your all access API token>"
export INFLUXDB_ORG="<your organization in InfluxDB Cloud Serverless>"
export INFLUXDB_HOST="<your cluster URL in InfluxDB Cloud Serverless>"
pip install -r <path_to_script>/requirements.txt
python3 <path_to_script>/measure.py
```

Example:

```bash
export INFLUXDB_TOKEN="3my7D...JIB4ezg=="
export INFLUXDB_ORG="Organization"
export INFLUXDB_HOST="https://eu-central-1-1.aws.cloud2.influxdata.com"
pip install -r ./requirements.txt
python3 ./measure.py
```

## Authors

- [@jani-heinikoski](https://github.com/jani-heinikoski)
- [@ViliAu](https://github.com/ViliAu)
