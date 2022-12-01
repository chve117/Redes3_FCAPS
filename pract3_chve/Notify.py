import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '
# Define params
rrdpath = '/home/chve117/Documentos/pract3-20221130T151730Z-001/pract3/RRD'
imgpath = '/home/chve117/Documentos/pract3-20221130T151730Z-001/pract3/IMG'
fname = 'trend.rrd'

mailsender = "dummycuenta3@gmail.com"
mailreceip = "dummycuenta3@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'dvduuffmlhspbmjj'

def send_alert_attached(subject,content,imagen):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imagen, 'rb')
    
    img = MIMEImage(fp.read())
    
    fp.close()
    
    msg.attach(MIMEText(content,'plain'))
    msg.attach(img)
    
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()


