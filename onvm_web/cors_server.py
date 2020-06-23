# Source: https://stackoverflow.com/questions/21956683/enable-access-control-on-simple-http-server

#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import json
import subprocess
import os
import signal

global pid
pid = -1

class CORSRequestHandler (SimpleHTTPRequestHandler):
    # normal CORS setup
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization')
        SimpleHTTPRequestHandler.end_headers(self)
    # handle post event
    def do_POST(self):
        # get request body and parse it into json format
        post_body = self.rfile.read(int(self.headers.get('content-length')))
        post_body_json = json.loads(post_body)

        # read the request body
        try:
            request_type = post_body_json['request_type']
        except KeyError:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # create json response
            response = json.dumps({'status': '500', 'message': 'missing request type'})
            self.wfile.write(str.encode(response))
            return None

        # setup response
        response = ""
        global pid
        # handle start nf chain request
        if request_type == "start":
            command = ['python', './config.py', './example_chain.json']
            try:
                # check if the process is already started
                if pid != -1:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'status': '403', 'message': 'process already started'})
                    self.wfile.write(str.encode(response))
                    return None
                # open a file to store nf chain output
                try:
                    log_file = open('${ONVM_HOME}/onvm_web/test.txt', 'w')
                except:
                    print("cannot open file test.txt")
                    return None

                # in order to run scripts correctly, must change dir to the example folder
                os.chdir('../examples/')
                p = subprocess.Popen(command, stdout=(log_file),\
                     stderr=log_file, universal_newlines=True)
                pid = p.pid
                self.send_response(200)

                # send response to react front end
                response = json.dumps({'status': '200', \
                    'message': 'success starting nfs', 'pid': str(pid)})

                # change the dir back for correct output
                os.chdir('../onvm_web/')
            except OSError:
                self.send_error(500)
                response = json.dumps({'status': '500', 'message': 'failed starting nfs'})
            finally:
                log_file.close()
        # handle stop nf chain request
        elif(request_type == "end"):
            try:
                # open the file to load nf information
                try:
                    log_file = open('${ONVM_HOME}/onvm_web/test.txt', 'r')
                except:
                    print("cannot open file test.txt")
                    return None
                # first kill all the nfs that's running in the background
                next_line = log_file.readline()
                while(next_line is not None and next_line != ""):
                    line_info = next_line.split(" ")
                    if(line_info[0] == "Pid"):
                        try:
                            os.kill(int(line_info[1]), signal.SIGKILL)
                        except OSError:
                            self.send_error(500)
                os.kill(pid, signal.SIGKILL)
                # reset pid
                pid = -1
                self.send_response(200)
            except OSError:
                self.send_error(500)
            finally:
                log_file.close()

        self.end_headers()
        self.wfile.write(str.encode(response))

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=8000)
