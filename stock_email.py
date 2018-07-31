import smtplib
import stock_checker
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import codecs

def stocks_email():
    stock_checker.get_stock_data()
    
    msg = MIMEMultipart('mixed')
    msg['Subject'] = 'Stocks update'

    stock_page = codecs.open('Stock data.html', 'r')
    msg_text = MIMEText(stock_page.read(), 'html')
    stock_page.close()
    msg.attach(msg_text)

    fp = open('BABA.png', 'rb')
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header('Content-ID', '<image1>')
    msg.attach(msg_img)

    fp = open('SSYS.png', 'rb')
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header('Content-ID', '<image2>')
    msg.attach(msg_img)

    fp = open('STM.png', 'rb')
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header('Content-ID', '<image3>')
    msg.attach(msg_img)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("XXXX", "XXXX")


    server.sendmail("XXXX", "XXXX", msg.as_string())
    server.quit()
                
stocks_email()
