from PIL import Image
import pyqrcode

def generate_qr_code(link):
    qrcode = pyqrcode.create(link)
    return qrcode.png('QRCode.png', scale = 7)

# Use example
qr_code = generate_qr_code('https://www.google.com.br/')
Image.open('QRCode.png')
