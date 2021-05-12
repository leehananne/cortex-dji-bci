# ====================================================================
#   global variables
# ====================================================================

command = " "

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
                "clientId": '5IDKFSE1znB1EpF7Qi59uUvb0QPzLHSVEE4oidkB',
                "clientSecret": 'LDe9kT0Y910eZBtvQcfv4P0udLaVl3WPtQz7NcUmqzcxFmDXVouO7UZ3VZ9AR55TFDXLI93m2vwjDSFv8Dz4TVTXt8rLWd7pfhLB56SgZSPRqLZQkEEHZJxu8OXkQBbu'
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
                "clientSecret": 'LDe9kT0Y910eZBtvQcfv4P0udLaVl3WPtQz7NcUmqzcxFmDXVouO7UZ3VZ9AR55TFDXLI93m2vwjDSFv8Dz4TVTXt8rLWd7pfhLB56SgZSPRqLZQkEEHZJxu8OXkQBbu',
                # "license": self.user['license'],
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

    def sub_request(self, stream):
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
                    print(command)                      # extracts out mental commands

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


def main():
    user = '5IDKFSE1znB1EpF7Qi59uUvb0QPzLHSVEE4oidkB'
    cortex = Cortex(user, False)

    cortex.do_prepare_steps()

    while 1:
        print("\n=========================================================================")
        print("\nenter selection: ")
        print("\n   1: get cortex info")
        print("\n   2: query profiles")
        print("\n   3: set up profiles (create, load, unload, save, rename, delete)")
        print("\n   4: subscribe to mental commands / control cursor")
        print("\n   5: records (create, stop or export)")
        print("\n   6: inject marker request")
        print("\n   7: disconnect headset")
        print("\n   8: quit\n")
        choice = input("choice (1-8): ")
        choice = int(choice)
        print("\n=========================================================================\n")

        while choice < 1 or choice > 8:
            print("key in a number from 1-8\n")
            choice = input("choice (1-8): ")
            choice = int(choice)

        if choice == 1:
            cortex.get_cortex_info()
        elif choice == 2:
            cortex.query_profile()
        elif choice == 3:
            profile = input("\nenter profile name: ")
            print("enter selection: \n==========================================================")
            print("\n   1: create")
            print("\n   2: load")
            print("\n   3: unload")
            print("\n   4: save")
            print("\n   5: rename")
            print("\n   6: delete")
            print("\n==========================================================\n")
            profile_choice = input("choice (1-6): ")
            profile_choice = int(profile_choice)

            while profile_choice < 1 or profile_choice > 6:
                print("key in a number from 1-6\n")
                profile_choice = input("choice (1-6): ")
                profile_choice = int(profile_choice)

            if profile_choice == 1:
                profile_status = "create"
            elif profile_choice == 2:
                profile_status = "load"
            elif profile_choice == 3:
                profile_status = "unload"
            elif profile_choice == 4:
                profile_status = "save"
            elif profile_choice == 5:
                profile_status = "rename"
            elif profile_choice == 6:
                profile_status = "delete"

            cortex.setup_profile(profile, profile_status)

        elif choice == 4:
            # print("current profile: --------------------------------------------\n")
            cortex.getCurrentProfile()
            current_profile = cortex.current_profile_name
            print("\n   current profile: ", current_profile)
            current_ans = input("\nis this the desired profile to use? (y/n): ")
            print("\n")

            if current_ans == "n":
                cortex.setup_profile(current_profile, "unload")
                cortex.query_profile()
                current_profile = input("enter name of desired profile from above list: ")
                cortex.setup_profile(current_profile, "load")

        elif choice == 5:
            print("enter selection: \n==========================================================")
            print("\n   1: create")
            print("\n   2: stop")
            print("\n   3: export")
            print("\n==========================================================\n")
            records_choice = input("choice (1-3): ")
            records_choice = int(records_choice)

            while records_choice < 1 or records_choice > 3:
                print("key in a number from 1-3\n")
                records_choice = input("choice (1-3): ")
                records_choice = int(records_choice)

            if records_choice == 1:
                records_name = input("\nenter record name: ")
                cortex.create_record(records_name, None)
            elif records_choice == 2:
                cortex.stop_record()
            elif records_choice == 3:
                records_path = input("\ndesired path: ")
                print("stream types: \n==========================================================")
                print("\n   1: raw EEG data, contact quality of each EEG sensor, and markers")
                print("\n   2: motion data")
                print("\n   3: performance metric detection")
                print("\n   4: band powers of each EEG sensor")
                print("\n==========================================================\n")
                records_type = input("choice (1-4): ")
                records_type = int(records_type)

                while records_type < 1 or records_type > 4:
                    print("key in a number from 1-4\n")
                    records_type = input("choice (1-4): ")
                    records_type = int(records_type)

                if records_type == 1:
                    stream_type = "EEG"
                elif records_type == 2:
                    stream_type = "MOTION"
                elif records_type == 3:
                    stream_type = "PM"
                elif records_type == 4:
                    stream_type = "BP"

                records_format = input("\nrecords format (EDF/CSV): ")
                records_format = records_format.upper()

                while records_format != "EDF" or records_format != "CSV":
                    print("input EDF or CSV\n")
                    records_format = input("EDF or CSV? --------- ")
                if records_format == "CSV":
                    records_version = input("\ndesired CSV version (V1/V2) : ")

                record_id = cortex.record_id

                cortex.export_record(records_path, stream_type, records_format, records_version, record_id)
                # cortex.export_record(records_path, records_type, records_format, records_version)

        elif choice == 6:
            current_datetime = datetime.now()
            start_datetime = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=datetime.utc)
            time_delta = current_datetime - start_datetime
            time_delta = datetime.microsecond(time_delta)

            cortex.inject_marker_request(time_delta)

        elif choice == 7:
            cortex.disconnect_headset()

        elif choice == 8:
            break


if __name__ == "__main__":
    main()
