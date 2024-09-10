#!/usr/bin/python3

from socket import *

server_name="localhost"
server_port = 12001

http_request = f"GET /index.html HTTP/1.1\r\n" \
               f"Host: {server_name}\r\n" \
               f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" \
               f"Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\n" \
               f"Keep-Alive: 115\r\n" \
               f"Connection: keep-alive\r\n\r\n"

client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_name,server_port))
client_socket.send(http_request.encode())
modified_message = client_socket.recv(2048)
print("From server: ", modified_message.decode())
client_socket.close()
