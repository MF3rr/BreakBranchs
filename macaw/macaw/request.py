# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket

class MySocket:
    '''Responsável por criar e enviar dados'''
    def __init__(self, host, payload_bytes, port=80, buffer_size=1024):
        self.host = host
        self.port = port
        self.payload_bytes = payload_bytes
        self.buffer_size = buffer_size
        self.socket = socket.socket()
    
    def send_data(self):
        sock = self.socket
        sock.connect((socket.gethostbyname(self.host), self.port))
        sock.sendall(self.payload_bytes)
        cache = []
        while True:
            data = sock.recv(self.buffer_size)
            if not data:
                break
            cache.append(data)
        sock.close()
        response = b''.join(cache)
        return response

class Request:
  '''Monta os cabeçalhos de requisição'''
  def __init__(self, url):
    self.url = url
    
  def url_options(self):
    '''Monta o caminho'''
    url_split = self.url.split('/', 1)
    host = url_split[0]
    try:
      path = url_split[1]
    except:
      path = ''
    return host, path

  def GET(self):
    '''Metodo GET'''
    (host, path) = self.url_options()
    HEADERS = str(f'''GET /{path} HTTP/1.1\r\n
                      Host: {host}\r\n
                      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36\r\n
                      Referer: {host}\r\n\r\n''')
    payload_bytes = bytes(HEADERS, 'utf-8')
    requests = MySocket(host, payload_bytes)
    return requests.send_data()



# USE EXAMPLE
'''
url = 'google.com/search?q=gatos'
url1 = 'google.com'

request = Request(url1)
print(request.GET())
'''
