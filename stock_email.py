import smtplib
import stock_checker
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import codecs

stock_checker.pull_data()

msg = MIMEMultipart("mixed")
msg["Subject"] = "Stocks update"

stock_page = codecs.open("stock_data.html", "r")
msg_text = MIMEText(stock_page.read(), "html")
stock_page.close()
msg.attach(msg_text)

fp = open("AAPL.png", "rb")
msg_img = MIMEImage(fp.read())
fp.close()
msg_img.add_header("Content-ID", "<image1>")
msg.attach(msg_img)

fp = open("MSFT.png", "rb")
msg_img = MIMEImage(fp.read())
fp.close()
msg_img.add_header("Content-ID", "<image2>")
msg.attach(msg_img)

fp = open("TSLA.png", "rb")
msg_img = MIMEImage(fp.read())
fp.close()
msg_img.add_header("Content-ID", "<image3>")
msg.attach(msg_img)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("lestockupdates@gmail.com", "XXXXX")
server.sendmail("lestockupdates@gmail.com", "everett.lee@btinternet.com", msg.as_string())
server.quit()
