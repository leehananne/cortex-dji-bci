# Using the EMOTIV Cortex API to control the DJI RoboMaster EP

EMOTIV Cortex - the core piece of technology at EMOTIV which brings the brain computer interface to consumer. It is built on JSON and WebSockets, making it easy to access from a variety of programming languages and platforms. After using a third-party platform to establish a connection with RoboMaster EP, users can perform more complex and interesting operations on the EP robot through the plaintext SDK. 

> The code here is for Cortex version 2.0 or above. It is not valid for Cortex version 1.x.
> 
> The code here is written for the DJI RoboMaster EP, connected via Wi-Fi Networking Mode.

## Requirements
### Install the RoboMaster SDK
Have the RoboMaster SDK installed, following [these instructions](https://robomaster-dev.readthedocs.io/en/latest/python_sdk/installs.html)

### Programming Language
Ensure that the downloaded python.exe file is for 64-bit installation and the Python version is between **3.6.6 and 3.8.9**. Otherwise, you cannot use the DJI RoboMaster Python SDK properly due to compatibility issues.

The code is written in Python 3.8.8, which you can download from [Python](https://www.python.org/downloads/release/python-388/). 

The code was written on a Windows 10 64-bit machine.

## Usage

After obtaining the IP address of the RoboMaster, one must update the IP address into the files. 

This can be done by searching for **[ip_address]** in the code, and replacing it with the IP address of the robot - keeping the inverted commas. 

## Description
`cortex_dji.py`

Using the same CLI that [was used to control an on-screen cursor using commands from EMOTIV Cortex](https://github.com/leehananne/cortex-dji-bci/blob/master/cortex/cortex_cursor.py), this script now establishes a connection with the DJI RoboMaster EP via Wi-Fi Networking Mode, and executes movements according to the commands received from Emotiv's Cortex API. 

This code subscribes to the Mental Commands stream by default - one can change this by modifying the sub_request(self, stream) function in the Cortex class and is based on a training profile that has been trained on the following commands: **PUSH, PULL, LEFT, RIGHT**.

To **modify to your own commands**, **modify lines 350-358** accordingly. 

`cortex_dji_livestream.bat`

A batch file that runs `cortex_dji.py` and `rm_livestream.py` simultaneously, allowing the user to see the livestream of the DJI RoboMaster EP while it executes movements according to the commands received from Emotiv's Cortex API.

`robot_connection.py`

This is a python module that supports a basic networking connection methods for connecting robots - it needs to be in the same folder as the other files, else the other files will not work. For more information, click [here](https://github.com/dji-sdk/RoboMaster-SDK/tree/master/examples/plaintext_sample_code/RoboMasterEP/connection/network).

`rm_livestream.py`

Fetches the video stream from the DJI RoboMaster EP and displays it on screen - **this code does NOT fetch the audio stream**. 

The [decoders](https://github.com/dji-sdk/RoboMaster-SDK/tree/master/examples/plaintext_sample_code/RoboMasterEP/stream/decoder) for video and audio strams need to be installed, and can be done by following the documentation.

### More information
For information on how to connect in your desired fashion, refer to the [DJI RoboMaster Developer Page](https://robomaster-dev.readthedocs.io/en/latest/index.html)

