# EMOTIV Cortex API

EMOTIV Cortex - the core piece of technology at EMOTIV which brings the brain computer interface to consumer. It is built on JSON and WebSockets, making it easy to access from a variety of programming languages and platforms.

> The code here is for Cortex version 2.0 or above. It is not valid for Cortex version 1.x.

## Requirements
### Supported Platforms
Currently, Cortex is supported on the following platforms:
  
  - Windows 10 (64-bit only)
  - macOS 10.13 High Sierra or above
  - Linux Ubuntu 18.04 or above (Beta release, 64-bit only)
  - iOS 12 or above (Beta release)
  - Android 7.0 Nougat (API level 24) or above (Beta release)
  - Raspberry Pi OS - Debian version 10 (Beta release, 32-bit)

You can download the latest version of Cortex on the [EMOTIV Website](https://www.emotiv.com/get-started/). 

### Connect to the Cortex API
Information regarding supported headsets and how to start using the Cortex API can be found through [EMOTIV's documentation of the Cortex API](https://emotiv.gitbook.io/cortex-api/).

## Description

`cortex.py`

This code is based on a training profile that has been trained on the following commands: **PUSH, PULL, LEFT, RIGHT**. 

**To modify to your own commands**, modify **lines 350-358** accordingly.

Connects to the Emotiv Cortex API, following the API flow provided by Emotiv. This code subscribes to the **Mental Commands** stream by default - one can change this by modifying the `sub_request(self, stream)` function in the `Cortex` class.

It outputs a Command Line Interface displaying each step of the process. Choosing to subscribe to the Mental Command stream will prompt you to load a profile as recommended by Emotiv - the code will display all your training profiles, and you will have to enter the name of the desired profile when prompted.

`cortex_cursor.py`

Built on `cortex.py`, controls your on screen cursor using the PyAutoGUI module.


## Overview of Cortex API Flow
![alt text](https://gblobscdn.gitbook.com/assets%2F-LVaLrV9hH1eJbn-6OTd%2F-M8QqtwkSmhYUMPOQJgh%2F-M8R5tEmDnp-tghr3nhZ%2Fcortex-starting.jpg?alt=media&token=de2d5a6a-7c78-4eef-9888-d11a298cd61c)
