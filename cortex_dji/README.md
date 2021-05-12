# Using the EMOTIV Cortex API to control the DJI RoboMaster EP

After using a third-party platform to establish a connection with RoboMaster EP, users can perform more complex and interesting operations on the EP robot through the plaintext SDK. 

> The code here written for the DJI RoboMaster EP, connected via Wi-Fi Networking Mode.

## Requirements
### Install the RoboMaster SDK
Have the RoboMaster SDK installed, following [these instructions](https://robomaster-dev.readthedocs.io/en/latest/python_sdk/installs.html)

### Programming Language
Ensure that the downloaded python.exe file is for 64-bit installation and the Python version is between **3.6.6 and 3.8.9**. Otherwise, you cannot use the Python SDK properly due to compatibility issues.

You can download Python 3.8.8 from [Python](https://www.python.org/downloads/release/python-388/). 

The code was written on a Windows 10 64-bit machine.

## Usage

After obtaining the IP address of the RoboMaster, one must update the IP address into the files. 

This can be done by searching for **[ip_address]** in the code, and replacing it with the IP address of the robot - keeping the inverted commas. 

## Description
`robot_connection.py`

This is a python module that supports a basic networking connection methods for connecting robots - it needs to be in the same folder as the other files, else the other files will not work. For more information, click [here](https://github.com/dji-sdk/RoboMaster-SDK/tree/master/examples/plaintext_sample_code/RoboMasterEP/connection/network).

`rm_livestream.py`

Fetches the video stream from the DJI RoboMaster EP and displays it on screen - **this code does NOT fetch the audio stream**. 

The [decoders](https://github.com/dji-sdk/RoboMaster-SDK/tree/master/examples/plaintext_sample_code/RoboMasterEP/stream/decoder) for video and audio strams need to be installed, and can be done by following the documentation.

### More information
For information on how to connect in your desired fashion, refer to the [DJI RoboMaster Developer Page](https://robomaster-dev.readthedocs.io/en/latest/index.html)

