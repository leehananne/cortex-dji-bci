# ====================================================================
#   global variables
# ====================================================================

robot = False
msg = " "
command = " "
# ====================================================================
#   connection for DJI RoboMaster EP
# ====================================================================

import socket
import sys
import time
from robomaster import robot
from robomaster import camera
import threading
import numpy as np
import libh264decoder
import signal
import enum
import queue
from PIL import Image as PImage
import cv2

# In direct connection mode, the default IP address of the robot is 192.168.2.1 and the control command port is port 40923.
host = "[ip_address]"
port = 40923

address = (host, int(port))

# Establish a TCP connection with the control command port of the robot.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ====================================================================
#   set up of API flow
# ====================================================================

import websocket
from datetime import datetime
import json
import ssl
import time
import sys
import pyautogui

# define request id
QUERY_HEADSET_ID = 1
CONNECT_HEADSET_ID = 2
REQUEST_ACCESS_ID = 3
AUTHORIZE_ID = 4
CREATE_SESSION_ID = 5
SUB_REQUEST_ID = 6
SETUP_PROFILE_ID = 7
QUERY_PROFILE_ID = 8
TRAINING_ID = 9
DISCONNECT_HEADSET_ID = 10
CREATE_RECORD_REQUEST_ID = 11
STOP_RECORD_REQUEST_ID = 12
EXPORT_RECORD_ID = 13
INJECT_MARKER_REQUEST_ID = 14
SENSITIVITY_REQUEST_ID = 15
MENTAL_COMMAND_ACTIVE_ACTION_ID = 16
MENTAL_COMMAND_BRAIN_MAP_ID = 17
MENTAL_COMMAND_TRAINING_THRESHOLD = 18


class Cortex():
    def __init__(self, user, debug_mode=False):
        print("\n=========================================================================")
        print('\nconnecting to wss://localhost:6868 --------------------------------------')
        url = "wss://localhost:6868"

        self.ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})
        self.user = user
        self.debug = debug_mode

        print('connected ---------------------------------------------------------------')
        print("\n=========================================================================\n")

    def query_headset(self):
        print('querying headsets -------------------------------------------------------')
        query_headset_request = {
            "jsonrpc": "2.0",
            "id": QUERY_HEADSET_ID,
            "method": "queryHeadsets",
            "params": {}
        }

        self.ws.send(json.dumps(query_headset_request, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)

        self.headset_id = result_dic['result'][0]['id']
        if self.debug:
            print('query headset result', json.dumps(result_dic, indent=4))
            print(self.headset_id)

    def connect_headset(self):
        print('connecting headset ------------------------------------------------------')
        connect_headset_request = {
            "jsonrpc": "2.0",
            "id": CONNECT_HEADSET_ID,
            "method": "controlDevice",
            "params": {
                "command": "connect",
                "headset": self.headset_id
            }
        }

        self.ws.send(json.dumps(connect_headset_request, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('connect headset result', json.dumps(result_dic, indent=4))

    def request_access(self):
        print('requesting access -------------------------------------------------------')
        request_access_request = {
            "jsonrpc": "2.0",
            "method": "requestAccess",
            "params": {
                "clientId": '[clientId]',
                "clientSecret": '[clientSecret]'
            },
            "id": REQUEST_ACCESS_ID
        }

        self.ws.send(json.dumps(request_access_request, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print(json.dumps(result_dic, indent=4))

    def authorize(self):
        print('authorizing -------------------------------------------------------------')
        authorize_request = {
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {
                "clientId": self.user,
                "clientSecret": '[clientSecret]'
                                "debit": 5
        },
        "id": AUTHORIZE_ID
        }

        if self.debug:
            print('auth request \n', json.dumps(authorize_request, indent=4))

        self.ws.send(json.dumps(authorize_request))

        while True:
            result = self.ws.recv()
            result_dic = json.loads(result)
            if 'id' in result_dic:
                if result_dic['id'] == AUTHORIZE_ID:
                    if self.debug:
                        print('auth result \n', json.dumps(result_dic, indent=4))
                    # print(result_dic)
                    self.auth = result_dic["result"]["cortexToken"]
                    break

    def create_session(self, auth, headset_id):
        print('creating session --------------------------------------------------------')
        create_session_request = {
            "jsonrpc": "2.0",
            "id": CREATE_SESSION_ID,
            "method": "createSession",
            "params": {
                "cortexToken": self.auth,
                "headset": self.headset_id,
                "status": "active"
            }
        }

        if self.debug:
            print('create session request \n', json.dumps(create_session_request, indent=4))

        self.ws.send(json.dumps(create_session_request))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('create session result \n', json.dumps(result_dic, indent=4))

        # print(result_dic)
        self.session_id = result_dic['result']['id']

    def close_session(self):
        print('closing session ---------------------------------------------------------')
        close_session_request = {
            "jsonrpc": "2.0",
            "id": CREATE_SESSION_ID,
            "method": "updateSession",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "status": "close"
            }
        }

        self.ws.send(json.dumps(close_session_request))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('close session result \n', json.dumps(result_dic, indent=4))

    def get_cortex_info(self):
        print('getting cortex info -----------------------------------------------------')
        get_cortex_info_request = {
            "jsonrpc": "2.0",
            "method": "getCortexInfo",
            "id": 100
        }

        self.ws.send(json.dumps(get_cortex_info_request))
        result = self.ws.recv()
        if self.debug:
            print(json.dumps(json.loads(result), indent=4))

    def do_prepare_steps(self):
        self.query_headset()
        self.connect_headset()
        self.request_access()
        self.authorize()
        self.create_session(self.auth, self.headset_id)

    # ====================================================================
    #   profiles -> needs to be loaded for mental commands
    # ====================================================================

    # queryProfile to list the profiles of the current user

    def query_profile(self):
        print('querying profiles -------------------------------------------------------\n')
        query_profile_json = {
            "jsonrpc": "2.0",
            "method": "queryProfile",
            "params": {
                "cortexToken": self.auth,
            },
            "id": QUERY_PROFILE_ID
        }

        if self.debug:
            print('query profile request \n', json.dumps(query_profile_json, indent=4))
            print('\n')

        self.ws.send(json.dumps(query_profile_json))

        result = self.ws.recv()
        result_dic = json.loads(result)

        # print('query profile result\n',result_dic)
        # print('\n')

        profiles = []
        for p in result_dic['result']:
            profiles.append(p['name'])

        print('profile names -----------------------------------------------------------')
        # print(*profiles, sep = "\n")

        for i, val in enumerate(profiles):
            print("\n   ", val, "\n")
            # print(i+1, " : ", val)

        return profiles

    # setupProfile to manage the profiles

    def setup_profile(self, profile_name, status):
        # print('setup profile -----------------------------------------------------------')
        setup_profile_json = {
            "jsonrpc": "2.0",
            "method": "setupProfile",
            "params": {
                "cortexToken": self.auth,
                "headset": self.headset_id,
                "profile": profile_name,
                "status": status
            },
            "id": SETUP_PROFILE_ID
        }

        if self.debug:
            print('setup profile json:\n', json.dumps(setup_profile_json, indent=4))
            print('\n')

        self.ws.send(json.dumps(setup_profile_json))

        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('result \n', json.dumps(result_dic, indent=4))
            print('\n')

    # getCurrentProfile

    def getCurrentProfile(self):
        print('getting current profile -------------------------------------------------')
        getcurrent_profile_json = {
            "jsonrpc": "2.0",
            "method": "getCurrentProfile",
            "params": {
                "cortexToken": self.auth,
                "headset": self.headset_id
            },
            "id": 1
        }

        if self.debug:
            print('get current profile json:\n', json.dumps(getcurrent_profile_json, indent=4))
            print('\n')

        self.ws.send(json.dumps(getcurrent_profile_json))

        result = self.ws.recv()
        result_dic = json.loads(result)
        Cortex.current_profile_name = result_dic['result']['name']

        if self.debug:
            print('result \n', json.dumps(result_dic, indent=4))
            print('\n')

    # ====================================================================
    #   subscribing to a session
    #
    #   all the subscriptions of a session are automatically
    #   cancelled when the session is closed
    # ====================================================================

    def sub_request(self, stream, dji, cursor):
        print('\nsubscribe request -------------------------------------------------------\n')
        sub_request_json = {
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "streams": ["com"]  # ----------------------------------------------> mental command stream
            },
            "id": SUB_REQUEST_ID
        }

        self.ws.send(json.dumps(sub_request_json))

        if 'sys' in stream:
            self.new_data = self.ws.recv()
            print(json.dumps(self.new_data, indent=4))
            print('\n')
        else:
            # result = self.ws.recv
            print("commands ----------------------------------------------------------------\n")
            while True:
                self.new_data = self.ws.recv()
                # print(self.new_data)
                result = self.new_data
                result_dic = json.loads(result)

                if "com" in result_dic:
                    command = result_dic['com'][0]
                    print(command)
                    if command == "left":
                        msg = "chassis move x -0.1;"
                    elif command == "right":
                        msg = "chassis move z 90;"
                    elif command == "push":
                        msg = "chassis move x 0.1;"
                    elif command == "pull":
                        msg = "chassis move x -0.1;"
                    elif command == "neutral":
                        msg = "chassis move  z 0;"

                    # Send control commands to the robot.
                    s.send(msg.encode('utf-8'))

                    try:
                        # Wait for the robot to return the execution result.
                        buf = s.recv(1024)
                        print(buf.decode('utf-8'))
                    except socket.error as e:
                        print("Error receiving :", e)
                        sys.exit(1)
                    if not len(buf):
                        break

    # ====================================================================
    #   records and markers
    # ====================================================================

    def create_record(self, record_name, record_description):
        print('creating record ---------------------------------------------------------')
        create_record_request = {
            "jsonrpc": "2.0",
            "method": "createRecord",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "title": record_name,
                "description": record_description
            },

            "id": CREATE_RECORD_REQUEST_ID
        }

        self.ws.send(json.dumps(create_record_request))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('start record request \n',
                  json.dumps(create_record_request, indent=4))
            print('start record result \n',
                  json.dumps(result_dic, indent=4))

        self.record_id = result_dic['result']['record']['uuid']

    def stop_record(self):
        print('stopping record ---------------------------------------------------------')
        stop_record_request = {
            "jsonrpc": "2.0",
            "method": "stopRecord",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id
            },

            "id": STOP_RECORD_REQUEST_ID
        }

        self.ws.send(json.dumps(stop_record_request))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('stop request \n',
                  json.dumps(stop_record_request, indent=4))
            print('stop result \n',
                  json.dumps(result_dic, indent=4))

    def export_record(self,
                      folder,
                      stream_types,
                      export_format,
                      export_version,
                      record_ids):
        print('exporting record --------------------------------------------------------')
        export_record_request = {
            "jsonrpc": "2.0",
            "id": EXPORT_RECORD_ID,
            "method": "exportRecord",
            "params": {
                "cortexToken": self.auth,
                "folder": folder,
                "format": export_format,
                "streamTypes": stream_types,
                "recordIds": record_ids
            }
        }

        # "version": export_version,
        if export_format == 'CSV':
            export_record_request['params']['version'] = export_version

        if self.debug:
            print('export record request \n',
                  json.dumps(export_record_request, indent=4))

        self.ws.send(json.dumps(export_record_request))

        # wait until export record completed
        while True:
            time.sleep(1)
            result = self.ws.recv()
            result_dic = json.loads(result)

            if self.debug:
                print('export record result \n',
                      json.dumps(result_dic, indent=4))

            if 'result' in result_dic:
                if len(result_dic['result']['success']) > 0:
                    break

    def inject_marker_request(self, marker):
        print('injecting marker --------------------------------------------------------')
        inject_marker_request = {
            "jsonrpc": "2.0",
            "id": INJECT_MARKER_REQUEST_ID,
            "method": "injectMarker",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "label": marker['label'],
                "value": marker['value'],
                "port": marker['port'],
                "time": marker['time']
            }
        }

        self.ws.send(json.dumps(inject_marker_request))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('inject marker request \n', json.dumps(inject_marker_request, indent=4))
            print('inject marker result \n',
                  json.dumps(result_dic, indent=4))

    # ====================================================================
    #   other
    # ====================================================================

    def disconnect_headset(self):
        print('disconnecting headset ---------------------------------------------------')
        disconnect_headset_request = {
            "jsonrpc": "2.0",
            "id": DISCONNECT_HEADSET_ID,
            "method": "controlDevice",
            "params": {
                "command": "disconnect",
                "headset": self.headset_id
            }
        }

        self.ws.send(json.dumps(disconnect_headset_request))

        # wait until disconnect completed
        while True:
            time.sleep(1)
            result = self.ws.recv()
            result_dic = json.loads(result)

            if self.debug:
                print('disconnect headset result', json.dumps(result_dic, indent=4))

            if 'warning' in result_dic:
                if result_dic['warning']['code'] == 1:
                    break


# ===============================================================================================================

def dji_robomaster_ep():
    print("connecting ---------------------------------------------------------------")
    s.connect(address)
    print("connected ----------------------------------------------------------------")

    msg = "command;"
    s.send(msg.encode('utf-8'))

    print("ready -------------------------------------------------------------------")


def main():
    user = '5IDKFSE1znB1EpF7Qi59uUvb0QPzLHSVEE4oidkB'
    cortex = Cortex(user, False)

    cortex.do_prepare_steps()

    while 1:
        dji_robomaster_ep()
        cortex.sub_request("com", True, False)


if __name__ == "__main__":
    main()
