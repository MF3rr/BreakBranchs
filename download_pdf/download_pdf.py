import requests
import os

def download_pdf(url, name='default', save_path=os.getcwd()):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'{save_path}/{name}.pdf', 'wb') as file:
            file.write(response.content)
            return 'OK'
    else:
      return 'download bad'

#use
url = 'https://doem.org.br/ba/modelo/arquivos/pdfviewer/0b517cdc5f9850e3782051c82e7f3234?name=lorem-ipsum.pdf'
print(download_pdf(url, 'lorem_ipsum'))
