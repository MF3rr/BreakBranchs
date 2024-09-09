# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket
import subprocess

def port_scanner(target, ports=[port for port in range(0,65535,1)]):
  '''toc toc... toc toc... escaneia ips a procura de portas abertas'''
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

def get_interfaces():
  '''captura as interfaces e relaciona com ips'''
  interfaces = [hex(interface[0]) for interface in socket.if_nameindex()] # transforma as interfaces em hex
  arp_out = subprocess.run('arp -a', stdout=subprocess.PIPE, text=True).stdout # saida do comando arp

  interface_ip = []
  for line in arp_out.splitlines():
    if 'Interface' in line:
      hex_interface = (str(line[line.index('x')-1:]).replace('\n','').strip()) # busca por interfaces
      if hex_interface in interfaces:
        cache = [hex_interface, str(line[line.index(':')+1:line.index('-')-1]).strip()]
        interface_ip.append(cache) # relaciona interface e ip
        cache = []
  return interface_ip


'''
# USE EXAMPLE
print(get_interfaces())
'''

'''
Note,
Isto é util para uso em sniffers quando não se conta com o IP.
Com isto é possivel efetuar uma varredura completa das portas.
'''
