import smtplib
import email.message

class sendMail():
  def __init__(self, from_, to, subject, body):
    self.from_ = from_
    self.to = to
    self.subject = subject
    self.body = body

  def send_mail():
    '''envia o email'''
    body_mail = self.body # corpo do email
    msg = email.message.Message()
    msg['Subject'] = "Mensagem automática" # titulo
    msg['From'] = self.from_ # email de origem
    msg['To'] = self.to # email de destino
    password = 'Senha gerada com aplicativo' # senha de aplicativo gerado
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body_mail)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return 'OK'

# @title Exemplo de uso
mail = sendMail('brasilian@gmail.com', 'american@gmail.com', 'My Friend Pedros', 'Hello!')
mail.send_mail()
