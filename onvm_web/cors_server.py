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
        SimpleHTTPRequestHandler.end_headers(self)
    # handle post event
    def do_POST(self):
        # get request body and parse it into json format
        post_body = self.rfile.read(int(self.headers.get('content-length')))
        post_body_json = json.loads(post_body)

        try:
            request_type = post_body_json['request-type']
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

        if(request_type == "start"):
            command = ['python', './test.py']
            try:
                # check if the process is already started
                if(pid != -1):
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'status': '403', 'message': 'process already started'})
                    self.wfile.write(str.encode(response))
                    return None
                # start the process and save the pid
                p = subprocess.Popen(command)
                pid = p.pid
                self.send_response(200)
            except OSError:
                self.send_error(500)
        elif(request_type == "end"):
            try:
                os.kill(pid, signal.SIGKILL)
                # reset pid
                pid = -1
                self.send_response(200)
            except OSError:
                self.send_error(500)

        self.end_headers()
        self.wfile.write(str.encode(response))

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=8000)
