# Source: https://stackoverflow.com/questions/21956683/enable-access-control-on-simple-http-server

#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import json
import subprocess
import os
import signal
import shlex

global is_running
is_running = -1

class CORSRequestHandler(SimpleHTTPRequestHandler):
    # CORS setup
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization')
        SimpleHTTPRequestHandler.end_headers(self)

    # handle post event
    def do_POST(self):
        # get request body and parse it into json format
        post_body = self.rfile.read(int(self.headers.get('content-length')))
        post_body_json = json.loads(post_body)

        # parse request body
        try:
            request_type = post_body_json['request_type']
        except KeyError:
            # if the body does not have request_type field
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': '500', 'message': 'missing request type'})
            self.wfile.write(str.encode(response))
            return None

        # handle start nf chain requests
        if request_type == "start":
            self.start_nf_chain(post_body_json)
        # handle stop nf chain request
        elif request_type == "stop":
            self.stop_nf_chain()

    # handle options request
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # handle start NF chain event
    def start_nf_chain(self, request_body_json):
        global is_running
        command = ['python3', '../examples/config.py', '../examples/example_chain.json']
        try:
            # check if the process is already started
            if is_running != -1:
                self.send_response(403)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'status': '403', 'message': 'process already started'})
                self.wfile.write(str.encode(response))
                # setup return result
                return -1
            # start the process and change the state
            log_file = open('./test.txt', 'w+')
            os.chdir('../examples/')
            p = subprocess.Popen(command, stdout=(log_file), stderr=log_file, universal_newlines=True)
            is_running = 1
            # send success message
            self.send_response(200)
            response = json.dumps({'status': '200', 'message': 'success starting nfs', 'pid': str(p.pid)})
            # change back to web dir for correct output
            os.chdir('../onvm_web/')
            # setup return result
            result = 0
        except OSError:
            self.send_response(500)
            response = json.dumps({'status': '500', 'message': 'failed starting nfs'})
            # setup return result
            result = -1
        finally:
            log_file.close()
            self.end_headers()
            self.wfile.write(str.encode(response))
        return result

    def stop_nf_chain(self):
        global is_running
        message = []
        try:
            # open the log file to read the is_runnings of the nfs
            close_log_file = open('./log.txt', 'w+')
            with open('./test.txt', 'r') as log_file:
                log = log_file.readline()
                while(log is not None and log != ""):
                    log_info = log.split(" ")
                    if(log_info[0] == "Starting"):
                        command = 'ps -ef | grep sudo | grep speed_tester | grep -v "grep" | awk "{print $2}"'
                        pids = os.Popen(shlex.split(command), stdout=(close_log_file), stderr=close_log_file, universal_newlines=True)
                        pid_processes = pids.read()
                        if pid_processes != "":
                            pid_processes = pid_processes.split("\n")
                            message.append(pid_processes)
                            for i in pid_processes:
                                os.kill(int(i), signal.SIGKILL)
                    log = log_file.readline()
            # reset is_running
            is_running = -1
            self.send_response(200)
            response = json.dumps({'status': '200', 'message': 'stop nfs successed', "pids": message})
            result = 0
        except OSError:
            self.send_response(500)
            response = json.dumps({'status': '500', 'message': 'failed stopping nfs'})
            result = -1
        finally:
            self.end_headers()
            self.wfile.write(str.encode(response))
        return result

    def parst_request_file(self, request_body_json):
        try:
            data = request_body_json['data']
        except KeyError:
            # if the body does not have data field
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': '500', 'message': 'missing data'})
            self.wfile.write(str.encode(response))
            return None
        print(type(data))

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=8000)
