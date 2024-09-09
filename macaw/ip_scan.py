import socket
import struct
import time
import os
import select  # Adicionando a importação do módulo select

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
  sum = 0
  count_to = (len(source_string) // 2) * 2
  count = 0

  while count < count_to:
    this_val = source_string[count + 1] * 256 + source_string[count]
    sum = sum + this_val
    sum = sum & 0xffffffff
    count = count + 2

  if count_to < len(source_string):
    sum = sum + source_string[len(source_string) - 1]
    sum = sum & 0xffffffff

  sum = (sum >> 16) + (sum & 0xffff)
  sum = sum + (sum >> 16)
  answer = ~sum
  answer = answer & 0xffff
  answer = answer >> 8 | (answer << 8 & 0xff00)
  return answer

def create_packet(id):
  header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
  data = struct.pack('d', time.time())
  my_checksum = checksum(header + data)
  header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
  return header + data

def do_one_ping(dest_addr, timeout):
  icmp = socket.getprotobyname("icmp")
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp) # criando um socket cru com icmp
  except PermissionError as e:
    print("Permissão negada: você precisa de privilégios de administrador/root.")
    return

  my_id = os.getpid() & 0xFFFF
  packet = create_packet(my_id)
  sock.sendto(packet, (dest_addr, 1))
  delay = receive_ping(sock, my_id, timeout)
  sock.close()
  return delay

def receive_ping(sock, id, timeout):
  time_left = timeout
  while True:
    started_select = time.time()
    what_ready = select.select([sock], [], [], time_left)
    how_long_in_select = (time.time() - started_select)
    if what_ready[0] == []:
      return

    time_received = time.time()
    rec_packet, addr = sock.recvfrom(1024)
    icmp_ip_header = rec_packet[0:20]
    icmp_header = rec_packet[20:28]
    icmp_data = rec_packet[29:]
    type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)
    if packet_id == id:
      bytes_in_double = struct.calcsize('d')
      time_sent = struct.unpack('d', rec_packet[28:28 + bytes_in_double])[0]
      return time_received - time_sent

    time_left = time_left - how_long_in_select
    if time_left <= 0:
      return

def ping(targets=[], timeout=1):
  toc_toc_macaw = []
  for target in targets:  
    delay = do_one_ping(target, timeout)
    print(f'Pinging {target} using Python: {delay}')
    print('\n')
    attempts = 1
    while True:
      if attempts >= 3:
        break
      else:
        if delay == 'None':
          attempts +=1
        else:
          toc_toc_macaw.append(target)
          break
  return toc_toc_macaw
      

if __name__ == '__main__':
  ip_range_10 = [f'10.{block_1}.{block_2}.{block_3}' for block_1 in range(0,256,1) for block_2 in range(0,256,1) for block_3 in range(0,256,1)]
  ip_range_192 = [f'192.168.{block_1}.{block_2}' for block_1 in range(0,256,1) for block_2 in range(0,256,1)]

  print(ping(ip_range_192))
  