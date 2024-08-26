# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket

def port_scanner(target, ports=[port for port in range(0,65535,1)]):
  clcoding = socket.gethostbyname(target) # ip

  print(clcoding)

  for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1) # time
    result = sock.connect_ex((clcoding, port))
    if result == 0:
      print(f"Port {port} is open")
    else:
      print(f"Port {port} is closed")
    sock.close()

# USE
'''
port_scanner('google.com', [80])
'''
