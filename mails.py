from email.message import EmailMessage
import ssl
import smtplib
import imghdr

email_emisor = 'santiscano@gmail.com'
email_password = '123123'
email_receptor = 'alhdfajlfs@kjhfk.com'

asunto = 'mail desde udemy'
cuerpo = """
te envio un email
"""

em = EmailMessage()
em['FROM'] = email_emisor
em['to'] = email_receptor
em['subject'] = asunto
em.set_content(cuerpo)

# adjuntar imagen
with open('17.jpg', 'rb') as file:
    file_data = file.read()
    file_tipo = imghdr.what(file.name)
    file_nombre = file.name
em.add_attachment(file_data, filename=file_nombre, subtype=file_tipo, maintype='image')




context = ssl.create_default_context()

with smtplib.SMTP_SSL(host="smtp.gmail.com", port=587) as smtp:
    smtp.login(email_emisor, email_password)
    smtp.sendmail(email_emisor,email_receptor, em.as_string())



# OPCION 2
# https://myaccount.google.com/u/1/lesssecureapps
# en esta url hay que desabilitar la opcion

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage
from pathlib import Path


path = Path("11-modulos-nativos/Strategy.png")
mime_image = MIMEImage(path.read_bytes())
mensaje = MIMEMultipart()
mensaje["from"] = "santiscano@gmail.com"
mensaje["to"] = "stefacs14@gmail.com"
mensaje["subject"] = "este es el asunto del mensaje"
body = MIMEText("cuerpo del mensaje", "html")
mensaje.attach(body)
mensaje.attach(mime_image)

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smpt:
    smpt.ehlo() # esto nos permite identificarnos con el servidor smtp e identificar el nombre del dominio
    smpt.starttls() # transport layer security

    smpt.login("santiscano@gmail.com", "123")
    smpt.send_message(mensaje)
    print("mensaje enviado")


