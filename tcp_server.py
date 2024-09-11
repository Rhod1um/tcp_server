#!/usr/bin/python3

from socket import *
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime

now = datetime.now()
def formatted_date():
   return format_date_time(mktime(now.timetuple()))

try:
    with open('not-found.html', 'r') as file:
        not_found = file.read()
except FileNotFoundError:
    not_found = "<html><body><h1>File not found on the server</h1></body></html>"

try:
    with open('index.html', 'r') as file:
        index = file.read()
except FileNotFoundError:
    index = "<html><body><h1>File not found on the server</h1></body></html>"

try:
    with open('login.html', 'r') as file:
        login = file.read()
except FileNotFoundError:
    login = "<html><body><h1>File not found on the server</h1></body></html>"

index = f"HTTP/1.1 200 OK\r\n" \
                f"Date: {formatted_date()}\r\n" \
                f"Server: localhost\r\n" \
                f"Accept-Ranges: bytes\r\n" \
                f"Content-Length: {len(index.encode())}\r\n" \
                f"Keep-Alive: timeout=5, max=100\r\n" \
                f"Connection: Keep-Alive\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"{index}"

login = f"HTTP/1.1 200 OK\r\n" \
                f"Date: {formatted_date()}\r\n" \
                f"Server: localhost\r\n" \
                f"Accept-Ranges: bytes\r\n" \
                f"Content-Length: {len(login.encode())}\r\n" \
                f"Keep-Alive: timeout=5, max=100\r\n" \
                f"Connection: Keep-Alive\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"{login}"

not_found = f"HTTP/1.1 404 NOT FOUND\r\n" \
                f"Server: localhost\r\n" \
                f"Content-Length: {len(not_found.encode())}\r\n" \
                f"Connection: close\r\n" \
                f"Content-Type: text/html; charset=iso-8859-1\r\n\r\n" \
                f"{not_found}"

bad_request = f"HTTP/1.1 400 BAD REQUEST\r\n" \
                f"Server: localhost\r\n" \
                f"Content-Length: 0\r\n" \
                f"Connection: close\r\n" \

method_not_allowed = f"HTTP/1.1 405 METHOD NOT ALLOWED\r\n" \
                f"Server: localhost\r\n" \
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

def log_request(req, client_ip, status_code, response_size):
    lines = req.split('\r\n')
    request_line = lines[0]
    now = datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
    log_entry = f'{client_ip} - - [{now} +0100] "{request_line}" {status_code} {response_size}\n'
    with open('request.log', 'a') as file:
        file.write(log_entry)

# apache format: 10.0.0.153 - - [08/Mar/2004:10:48:06 -0800] "GET /cgi-bin/mailgraph.cgi/mailgraph_0.png HTTP/1.1" 200 7970

server_port = 8088
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print("The server is ready to receive")
while True:
    is_root_path = False
    conn_socket, client_address = server_socket.accept()
    req = conn_socket.recv(2048).decode()
    print(f"Request received from {client_address[0]}, {client_address[1]}: \n{req}")

    req_ls = req.split()
    method, path = req_ls[0], req_ls[1]

    if method != "GET":
        log_request(req, client_address, 400, len(not_found.encode()))
        conn_socket.send(method_not_allowed.encode())
        continue
    
    if is_bad_request(req):
        log_request(req, client_address[0], 405, len(bad_request.encode()))
        conn_socket.send(bad_request.encode())
        continue

    if path != "/" and path != "/login":
        log_request(req, client_address[0], 404, len(not_found.encode()))
        conn_socket.send(not_found.encode())
        continue
    elif path == "/":
        log_request(req, client_address[0], 200, len(index.encode()))
        conn_socket.send(index.encode())
        continue
    elif path == "/login":
        log_request(req, client_address[0], 200, len(login.encode()))
        conn_socket.send(login.encode())
        continue
    
    conn_socket.close()
server_socket.close()
