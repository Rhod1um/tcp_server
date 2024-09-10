#!/usr/bin/python3

from socket import *
import platform

user_agent = f"MyClient/1.0 (Python {platform.python_version()}; {platform.system()} {platform.release()})"

server_name="localhost"
server_port = 12001
client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_name,server_port))

http_request2 = """GET /index.html HTTP/1.1\r\nHost: servername\r\nUser-Agent: Firefox/3.6.10\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-us,en;q=0.5\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nKeep-Alive: 115\r\nConnection: keep-alive\r\n\r\n""".format(server_name)


http_request = f"GET /index.html HTTP/1.1\r\n" \
               f"Host: {server_name}\r\n" \
               f"User-Agent: {user_agent}\r\n" \
               f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" \
               f"Accept-Language: en-us,en;q=0.5\r\n" \
               f"Accept-Encoding: gzip,deflate\r\n" \
               f"Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\n" \
               f"Keep-Alive: 115\r\n" \
               f"Connection: keep-alive\r\n\r\n"


# /index.html path skal have / i starten da det er roden på serveren, denne mappe er roden på serveren
# det er http standard, / må ikke fjernes. 

client_socket.send(http_request.encode())
res = client_socket.recv(2048)
print("Response from server: ", res.decode())
client_socket.close()





