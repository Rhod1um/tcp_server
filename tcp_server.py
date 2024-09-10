#!/usr/bin/python3

from socket import *
import os
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime

now = datetime.now()
def formatted_date():
   return format_date_time(mktime(now.timetuple()))

with open('not-found.html', 'r') as file:
    data_not_found = file.read()

with open('index.html', 'r') as file:
    index = file.read()

with open('login.html', 'r') as file:
    login = file.read()

index = f"HTTP/1.1 200 OK\r\n" \
                f"Date: {formatted_date()}\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Accept-Ranges: bytes\r\n" \
                f"Content-Length: {len(index.encode())}\r\n" \
                f"Keep-Alive: timeout=10, max=100\r\n" \
                f"Connection: Keep-Alive\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"{index}"

login = f"HTTP/1.1 200 OK\r\n" \
                f"Date: {formatted_date()}\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Accept-Ranges: bytes\r\n" \
                f"Content-Length: {len(login.encode())}\r\n" \
                f"Keep-Alive: timeout=10, max=100\r\n" \
                f"Connection: Keep-Alive\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"{login}"

http_404 = f"HTTP/1.1 404 NOT FOUND\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Content-Length: {len(data_not_found.encode())}\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"Connection: close\r\n" \
                f"{data_not_found}"

bad_request = f"HTTP/1.1 400 BAD REQUEST\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Content-Length: 0\r\n" \
                f"Connection: close\r\n" \

method_not_allowed = f"HTTP/1.1 405 METHOD NOT ALLOWED\r\n" \
                f"Server: MyServer/1.0\r\n" \
                f"Content-Length: 0\r\n" \
                f"Connection: close\r\n" \
                
def is_bad_request(req):
    lines = req.split('\r\n')

    request_line_parts = lines[0].split(' ')
    if len(request_line_parts) != 3:
        return True 

    method = request_line_parts[0]
    if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
        return True

    version = request_line_parts[2]
    if not version.startswith('HTTP/'):
        return True 

    if 'HTTP/1.1' in version and not any(header.startswith('Host:') for header in lines[1:]):
        return True

    return False

def log_request(req):
    with open('request.log', 'a') as file:
        file.write(req)

server_port = 12003
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print("The server is ready to receive")
while True:
    is_root_path = False
    conn_socket, client_address = server_socket.accept()
    req = conn_socket.recv(2048).decode()
    print(f"Request received from {client_address[0]}, {client_address[1]}: \n{req}")
    log_request(req)

    req_ls = req.split()
    method, path = req_ls[0], req_ls[1]

    if method != "GET":
        conn_socket.send(method_not_allowed.encode())
        conn_socket.close()
        continue
    
    if is_bad_request(req):
        conn_socket.send(bad_request.encode())
        conn_socket.close()
        continue

    if path != "/" and path != "/login":
        conn_socket.send(http_404.encode())
    elif path == "/":
        conn_socket.send(index.encode())
    elif path == "/login":
        conn_socket.send(login.encode())
    
    """
    #req_ls = req.split()
    #print(req_ls)

    #if req_ls[1] == "/":
    #    is_root_path = True

    #filepath = req_ls[1].replace("/","")
    
    #filepath = filepath.replace("/","")

    if not os.path.isfile(filepath) and not is_root_path:
        conn_socket.send(http_404.encode())
    elif is_root_path:
        conn_socket.send(index.encode())
    elif req_ls[1] == "login":
        conn_socket.send(login.encode())
    """
    
    conn_socket.close()
server_socket.close()
