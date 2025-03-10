#  coding: utf-8 
import socketserver,os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        # Parsing data to get the request method and uri
        data= self.data.decode("utf-8").splitlines()
        data_list = data[0].split()
        uri = data_list[1]
        method = data_list[0]

        # Dictionary for status codes
        self.code = {
            "200": 'HTTP/1.1 200 OK\r\n',
            "301": "HTTP/1.1 301 Moved Permanently\r\n",
            "404": "HTTP/1.1 404 Not Found\r\n",
            "405": "HTTP/1.1 405 Method Not Allowed\r\n"
        }
        # Dictionary for content type
        self.content = {
            "html": "text/html\r\n",
            "css": "text/css\r\n"
        }
        # Check if the request method is GET as that is the only method allowed
        if method!="GET":
            self.code405()
            return

        else:
            if "css" not in uri and "index" not in uri:
                # Checking if the uri should go to the homepage
                if uri[-1] != "/":
                    self.code301(uri)
                    return
                # Concatenate the uri with the path to the homepage 
                else:
                    uri += "index.html"
        
        # Check if the file directory exists    
        file_dir = "./www"+uri
        if os.path.exists(file_dir):
            info = open(file_dir,'r').read()
            if ".html" in uri:
                self.code200(".html",info)
                return

            if ".css" in uri:
                self.code200(".css",info)
                return

        # If the file directory does not exist, return 404
        self.code404()
        return

    
    # Handling all the status codes
    def code404(self):
        self.request.sendall(bytearray("{code}".format(code=self.code["404"]),'utf-8'))
    def code200(self,uri,info):
        if uri == ".css":
            self.request.sendall(bytearray("{code}Content-Type: {content}".format(code=self.code["200"], content = self.content["css"]),'utf-8'))
            self.request.sendall(bytearray(info,'utf-8'))
        else:
            self.request.sendall(bytearray("{code}Content-Type: {content}".format(code=self.code["200"], content = self.content["html"]),'utf-8'))
            self.request.sendall(bytearray(info,'utf-8'))
            
    def code301(self, uri):
        self.request.sendall(bytearray("{code}Location: {uri}/".format(code = self.code["301"], uri = uri),'utf-8'))
        
    def code405(self):
        self.request.sendall(bytearray("{code}".format(code=self.code["405"]),'utf-8'))
        
  
if __name__ == "__main__":

    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
