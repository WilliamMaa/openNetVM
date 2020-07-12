# Source: https://stackoverflow.com/questions/21956683/enable-access-control-on-simple-http-server

#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import json
import subprocess
import os
import signal
import cgi

# use this variable to track if the nf is still running
# if the nf chain is running, 1
# if the nf chain is not running, -1
global is_running
is_running = -1


class CORSRequestHandler(SimpleHTTPRequestHandler):
    # CORS setup
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers',
                         'Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization')
        SimpleHTTPRequestHandler.end_headers(self)

    # handle post event
    def do_POST(self):
        # if request type is form-data
        if self.headers.get('content-type').split(";")[0] == 'multipart/form-data':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         }
            )
            for field in form.keys():
                field_item = form[field]
                # filename = field_item.filename
                filevalue = field_item.value
                # filesize = len(filevalue)
                with open("../examples/nf_chain_config.json", 'w+') as f:
                    f.write(str(filevalue, 'utf-8'))
            self.send_message(200)
            return None

        # get request body and parse it into json format
        post_body = self.rfile.read(int(self.headers.get('content-length')))
        post_body_json = json.loads(post_body)

        # parse request body
        try:
            request_type = post_body_json['request_type']
        except KeyError:
            # if the body does not have request_type field
            response = json.dumps(
                {'status': '500', 'message': 'missing request type'})
            self.send_message(500, response)
            return None

        # handle start nf chain requests
        if request_type == "start":
            self.start_nf_chain()
        # handle stop nf chain request
        elif request_type == "stop":
            self.stop_nf_chain()
        else:
            response = json.dumps(
                {'status': '403', 'message': 'unknown request'})
            self.send_message(403, response)

    # handle options request
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # handle start NF chain event
    def start_nf_chain(self):
        global is_running
        # check if the process is already started
        is_running = self.check_is_running()
        if is_running == 1:
            response = json.dumps(
                {'status': '403', 'message': 'process already started'})
            self.send_message(403, response)
            return None
        try:
            command = ['python3', '../examples/config.py',
                       '../examples/nf_chain_config.json']
            # start the process and change the state
            log_file = open('./log.txt', 'w+')
            os.chdir('../examples/')
            p = subprocess.Popen(command, stdout=log_file,
                                 stderr=log_file, universal_newlines=True)
            is_running = 1
            # send success message
            response_code = 200
            response = json.dumps(
                {'status': '200', 'message': 'start nfs successed', 'pid': str(p.pid)})
            # change back to web dir for correct output
            os.chdir('../onvm_web/')
        except OSError:
            response_code = 500
            response = json.dumps(
                {'status': '500', 'message': 'start nfs failed'})
        finally:
            log_file.close()
            self.send_message(response_code, response)

    # handle stop nf request
    def stop_nf_chain(self):
        global is_running
        try:
            # check if the process is already stopped
            is_running = self.check_is_running()
            if is_running == -1:
                response = json.dumps(
                    {'status': '500', 'message': 'nfs already stoped'})
                self.send_message(500, response)
                return None
            # open the log file to read the process name of the nfs
            with open('./log.txt', 'r') as log_file:
                log = log_file.readline()
                while log is not None and log != "":
                    log_info = log.split(" ")
                    if log_info[0] == "Starting":
                        # get the pids of the nfs
                        command = "ps -ef | grep sudo | grep " + \
                            log_info[1] + \
                            " | grep -v 'grep' | awk '{print $2}'"
                        pids = os.popen(command)
                        pid_processes = pids.read()
                        if pid_processes != "":
                            pid_processes = pid_processes.split("\n")
                            for i in pid_processes:
                                if i != "":
                                    os.kill(i, signal.SIGKILL)
                    log = log_file.readline()
            # reset is_running
            is_running = -1
            response_code = 200
            response = json.dumps(
                {'status': '200', 'message': 'stop nfs successed'})
        except OSError:
            response_code = 500
            response = json.dumps(
                {'status': '500', 'message': 'stop nfs failed'})
        finally:
            self.clear_log()
            self.send_message(response_code, response)

    # send response message
    def send_message(self, response_code, message=None):
        self.send_response(response_code)
        self.end_headers()
        if message is not None:
            self.wfile.write(str.encode(message))

    # check if the nf is running
    def check_is_running(self):
        with open('./log.txt', 'r+') as log_file:
            log = log_file.readline()
            if log is None or log == "":
                return -1
            while log is not None and log != "":
                print("in checking")
                log_info = log.split(" ")
                if log_info[0] == "Error" or log_info[0] == "Exiting...":
                    return -1
                log = log_file.readline()
        return 1

    # clear output log
    def clear_log(self):
        with open('./log.txt', 'r+') as log_file:
            log_file.seek(0)
            log_file.truncate()


if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=8000)
