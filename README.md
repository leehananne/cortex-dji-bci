# cortex-dji-bci

## Description
Control and command a DJI RoboMaster EP using Mental Commands fetched from EMOTIV's Cortex API. The description of the `cortex`, `dji-robomaster` and `cortex-dji` folders can be found by clicking on them. 

## Requirements
### Cortex API only

As the EMOTIV Cortex API is a WebSocket server that uses the JSON-RPC protocol, any version of Python that supports `websocket-client` can be used. The description for it can be found [here](https://pypi.org/project/websocket-client/). 

The latest version of Python (as of March 2021), 3.9.2 was used to write and test the code in the `cortex` folder. Python 3.9.2 can be downloaded [here](https://www.python.org/downloads/release/python-392/).

There are also prerequisites that need to be met before the Cortex API can be used, such as an [EmotivID, License and Cortex App](https://emotiv.gitbook.io/cortex-api/#prerequisites).

The attached code prints out the name of the mental command and the power of it when a subscription request is sent to Cortex. Other data such as the sessionId and time are not printed, and will need to be extracted from the data sample object if desired.

### DJI RoboMaster only

The Python.exe file needs to be for 64-bit installation and the version must be **between 3.6.6 and 3.8.9**. Otherwise, the DJI RoboMaster Python SDK cannot be properly used due to compatibility issues. 

Instructions to set up the necessary programming environment can be found at [DJI's RoboMaster Development Guide](https://robomaster-dev.readthedocs.io/en/latest/code_env_setup.html). 

Python 3.8.8 was used to write and test the code in the `dji_robomaster` folder. This version of Python can be downloaded [here](https://www.python.org/downloads/release/python-388/). 

The RoboMaster application also needs to be installed to allow the DJI RoboMaster EP to connect via Wi-Fi router mode using a QR code that will be generated in the application. It can be downloaded [here](https://www.dji.com/sg/downloads/softwares/robomaster-win).

### Cortex and DJI RoboMaster

To cater to the DJI RoboMaster Plaintext SDK, Python 3.8.8 was used to write and test the code. This version of Python can be downloaded [here](https://www.python.org/downloads/release/python-388/). 

The requirements for both the Cortex API and DJI RoboMaster mentioned above must be met.

## Usage

To utilise the code, the following values need to be found and replaced accordingly. 

For the Cortex API, it will be:
- [clientId]
- [clientSecret]

For the DJI RoboMaster, it will be:
- [ip_address]
