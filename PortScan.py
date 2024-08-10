import socket

def port_scanner(target, ports):
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

# uso
target = "google.com" # dominio a ser verificado
ports = [21, 22, 80, 443] # portas que deseja verificar
port_scanner(target, ports)
