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

- To send example measurements to the InfluxDB database you previously set up, run the measurement_sample_gen.py script in your terminal (cd to the /sensor directory first):

    1. Install dependencies first with

    ```bash
    pip install -r ./requirements.txt
    ```

    2. Set the required environment variables

    ```bash
    export INFLUXDB_TOKEN="<your all access API token>"
    export INFLUXDB_ORG="<your organization in InfluxDB Cloud Serverless>"
    export INFLUXDB_HOST="<your cluster URL in InfluxDB Cloud Serverless>"
    ```

    3. Run the script

    ```bash
    python3 ./measurement_sample_gen.py
    ```

    Example:

    ```bash
    pip install -r ./requirements.txt
    export INFLUXDB_TOKEN="3my7D...JIB4ezg=="
    export INFLUXDB_ORG="Organization"
    export INFLUXDB_HOST="https://eu-central-1-1.aws.cloud2.influxdata.com"
    python3 ./measurement_sample_gen.py
    ```

    4. You're done! You should now have example data from the past week based on the Sense HAT emulator's values. The script makes the air temperature decrease linearly with a small amount of randomness introduced along with colder night temperatures.
 
## Visualization script

The visualization script is found in the graph folder. It runs on Windows platform (tested on Windows 10) using Python 3. To run the script, perform the following steps:

1. Install dependencies in the graph folder first with

    ```bat
    pip install -r ./requirements.txt
    ```

2. Set the required environment variables

    ```bat
    set INFLUXDB_TOKEN="<your all access API token>"
    set INFLUXDB_ORG="<your organization in InfluxDB Cloud Serverless>"
    set INFLUXDB_HOST="<your cluster URL in InfluxDB Cloud Serverless>"
    ```

3. Run the script
    ```bat
    python3 ./graph_gen.py
    ```

4. You're done! matplotlib-module should provide you with graphs representing the data from the database.


## Authors

- [@jani-heinikoski](https://github.com/jani-heinikoski)
- [@ViliAu](https://github.com/ViliAu)

