#!/usr/bin/python3

from socket import *
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import os

now = datetime.now()
def formatted_date():
   return format_date_time(mktime(now.timetuple()))
last_modified_date = formatted_date

data = "<html><body><h1>something</h1></body></html>"
data_not_found = "<html><body><h1>Not found!</h1></body></html>"
data_bad_request = "<html><body><h1>Bad request</h1></body></html>"

http_400 = f"HTTP/1.1 400 BAD REQUEST   \r\n" \
                f"Date: {formatted_date()}\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Content-Length: 0\r\n" \
                f"Connection: close\r\n\r\n" \

http_404 = f"HTTP/1.1 404 NOT FOUND\r\n" \
                f"Date: {formatted_date()}\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Content-Length: {len(data_not_found.encode())}\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"Connection: close\r\n" \
                f"{data_not_found}"

http_200 = f"HTTP/1.1 200 ok\r\n" \
                f"Date: {formatted_date()}\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Last-Modified: {last_modified_date}\r\n" \
                f"ETag: \"34aa387-d-1568eb00\"\r\n" \
                f"Accept-Ranges: bytes\r\n" \
                f"Content-Length: {len(data.encode())}\r\n" \
                f"Keep-Alive: timeout=10, max=100\r\n" \
                f"Connection: Keep-Alive\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"{data}"

def is_not_found(filepath):
    if not os.path.isfile(filepath):
        return True
    else:
        return False

def is_bad_request(request):
    # Split the request into lines
    lines = request.split('\r\n')

    # Check if the request line has three parts
    request_line_parts = lines[0].split(' ')
    if len(request_line_parts) != 3:
        return True  # Bad request

    # Check for a valid method
    method = request_line_parts[0]
    if method not in ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS']:
        return True  # Bad request

    # Check for the HTTP version
    version = request_line_parts[2]
    if not version.startswith('HTTP/'):
        return True  # Bad request

    # Check for the presence of the Host header in HTTP/1.1 requests
    if 'HTTP/1.1' in version and not any(header.startswith('Host:') for header in lines[1:]):
        return True  # Bad request

    # Additional checks can be added here

    return False  # Request is not bad
    

def get_resource(filepath):
    with open(filepath, 'rb') as file:
        content = file.read()

    response_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Date: {}\r\n"
        "Content-Length: {}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).format(formatted_date(), len(content))

    return response_headers, content

server_port = 12001
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind(('',server_port))
server_socket.listen(1)
print("The server is ready to receive")
while True:
    conn_socket, client_address = server_socket.accept()
    req = conn_socket.recv(2048).decode()
    print(f"Request received from {client_address}: \n{req}")
    
    response = None
    
    if is_bad_request(req):
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"
    
    req_ls = req.split()
    
    filepath = req_ls[1]
    filepath = filepath.replace("/","")
    get_resource(filepath)
    if req_ls[0] == "GET":
        headers, file_content = get_resource(filepath)
        
    conn_socket.sendall(headers.encode() + (file_content))
    conn_socket.close()
server_socket.close()




