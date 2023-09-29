#  coding: utf-8 
import socketserver

# Copyright [2023] [Wanlin Zheng]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #handle empty bytearray
        if self.data == b"":
            responseCode = 'HTTP/1.1 404 Not Found\r\n'
            header = "Content-Type: text/html/css\r\n Connection: close\r\n\r\n"
            response = responseCode + header + "<html><body>Error 404: Page not found</body></html> "
            self.request.sendall(bytearray(response, "utf-8"))
            return
    
        #parse request
        data = self.data.decode("utf-8")
        data = data.split()

        #send method not allowed error 405
        if data[0] != "GET":
            print("SENDING 405 \n")
            responseCode = 'HTTP/1.1 405 Not Method Not Allowed\r\n'
            header = "Content-Type: text/html\r\n Connection: close\r\n\r\n"
            response = responseCode + header + "<html><body>Error 405: Method Not allowed</body></html> "
            self.request.sendall(bytearray(response, "utf-8"))
            return

        # initialize variables
        filePath = ""
        contentType = ""
        response = bytearray("OK","utf-8")

        #handle css requests 
        if data[1] == "/base.css":
            filePath = "www/base.css"
            contentType = "Content-Type: text/css\r\n"
        elif data[1] == "/deep/deep.css":
            filePath = "www/deep/deep.css"
            contentType = "Content-Type: text/css\r\n"
        #handle 301 redirect cases
        elif data[1] == "/deep" or data[1] == "www/deep" :
            responseCode = "HTTP/1.0 301 Moved Permanently\r\n"
            header = "Location: http://127.0.0.1:8080/deep/"
            response = responseCode + header
            self.request.sendall(bytearray(response, "utf-8"))
            return
        else:
            if data[1][-10:] == "index.html":
                filePath = "www" + data[1]
            else:
                filePath = "www" + data[1] + "index.html"
            contentType = "Content-Type: text/html\r\n"

        if filePath != "":
            try:
                responseCode = "HTTP/1.0 200 OK\r\n"
                header = contentType + "Connection: close\r\n\r\n"
                response = responseCode + header
                #read html
                file = open(filePath,"r")
                for line in file:
                    response = response + line

                self.request.sendall(bytearray(response, "utf-8"))
            except FileNotFoundError: # send 404
                responseCode = 'HTTP/1.1 404 Not Found\r\n'
                header = "Content-Type: text/html/\r\n Connection: close\r\n\r\n"
                response = responseCode + header + "Error 404: Page not found"
                self.request.sendall(bytearray(response, "utf-8"))
            except NotADirectoryError:# send 404 
                responseCode = 'HTTP/1.1 404 Not Found\r\n'
                header = "Content-Type: text/html/\r\n Connection: close\r\n\r\n"
                response = responseCode + header + "Error 404: Page not found"
                self.request.sendall(bytearray(response, "utf-8"))
        else: # send 404
            responseCode = 'HTTP/1.1 404 Not Found\r\n'
            header = "Content-Type: text/html/\r\n Connection: close\r\n\r\n"
            response = responseCode + header + "Error 404: Page not found"
            self.request.sendall(bytearray(response, "utf-8"))

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
