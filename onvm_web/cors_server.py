# Source: https://stackoverflow.com/questions/21956683/enable-access-control-on-simple-http-server

#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler, test
# import json

class CORSRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    # def do_POST(self):
    #     post_body = self.rfile.read(int(self.headers['Content-Length']))
    #     print(post_body)
    #     post_body_json = json.loads(post_body);
    #     print(post_body_json)

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=8000)
