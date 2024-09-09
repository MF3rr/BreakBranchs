# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket
import struct
from ctypes import *

import subprocess

import threading
import queue

# Trecho extraído de Black Hat Python
class IP(Structure):
    _fields_ = [
      ("ihl", c_ubyte, 4),
      ("version", c_ubyte, 4),
      ("tos", c_ubyte),
      ("len", c_ushort), # tamanho
      ("id", c_ushort),
      ("offset", c_ushort),
      ("ttl", c_ubyte), # time to live
      ("protocol_num", c_ubyte), 
      ("checksum", c_ushort), # verificacao de integridade
      ("src", c_uint32), # porta origem
      ("dst", c_uint32) # porta destino
    ]

    def __new__(cls, socket_buffer=None):
      return cls.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
      # Mapa de protocolos
      self.protocol_map = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
      self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))  # origem
      self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))  # destino
      # Obter o nome do protocolo
      self.protocol = self.protocol_map.get(self.protocol_num, str(self.protocol_num))

class ICMP(Structure):
    _fields_ = [
      ('type', c_ubyte),
      ('code', c_ubyte),
      ('checksum', c_ushort),
      ('unused', c_ushort),
      ('next_hop_mtu', c_ushort)
    ]

    def __new__(self, socket_buffer):
      return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer):
      pass
# Fim do trecho extraido de Black Hat Python

def sniffer(host=[socket.gethostbyname(socket.gethostname())], port=None, codec='utf-8'):
  # >> socket.gaierror: [Errno 11001] getaddrinfo failed
  # Interface de rede pública
  # Cria um socket com interface pública
  print(host)
  sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
  sock.bind((host, port))
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)  # Inclui os cabeçalhos
  sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)  # ativa a promiscuidade

  cache = [] # armazenamento
  while True:  # Mantém-se escutando até que seja finalizado
    data = sock.recv(65565)
    if not data: # se não estiver mais nada sendo recebido
      break
    else:
      ip_header = IP(data[:20])
      content = data[21:] # conteudo
      if ip_header == 'ICMP':
        offset = ip_header.ihl * 4 # calcula onde comeca o ICMP
        buff = data[offset: offset + sizeof(ICMP)]
        icmp_header = ICMP(buff)
        print(icmp_header)
        print(content)
        print()
      else:
        print(f'Protocolo: {ip_header.protocol} | Origem: {ip_header.src_address} Destino: {ip_header.dst_address}')
        print(content)
        print()
    cache.append(data) # armazena os pacotes recebidos
  sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF) # desativa a promiscuidade

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


# USE EXAMPLE

# Criando o trabalho
def creating_work(interfaces, queue_process):
  for interface in interfaces:
    print(f'Adicionando inteface {interface [0]} à fila.')
    queue_process.put(interface[1])

# Trabalhando
def consuming_labor(queue_process, port=0, codec='ascii'):
  while True:
    ip = queue_process.get()
    print(f'Escutando IP {ip}')
    sniffer(ip, codec)
    queue_process.task_done()

queue_process = queue.Queue() # criando a fila

# Construindo o Thread
creating_work_thread = threading.Thread(target=creating_work, args=(get_interfaces(), queue_process,))
consuming_labor_thread = threading.Thread(target=consuming_labor, args=(queue_process,))

# Iniciando
creating_work_thread.start()
consuming_labor_thread.start()

# Finalizado
creating_work_thread.join()
consuming_labor_thread.join()







