import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def meetstartup():
   sender_email = "examplemsit@gmail.com"
   receiver_email = "tanmayarora118@gmail.com"
   password = "smwtujbcmobbmbda"

   message = MIMEMultipart("alternative")
   message["Subject"] = "Congratulation!! we have an investor "
   message["From"] = sender_email
   message["To"] = receiver_email


   text = """

Dear Founder,

All your efforts in profile building had to pay, An investor is ready to back in your vision with your start-up
We did our job now its your turn to grab the deal  
Go on and give your best
You can join a vitual reality meet on http://localhost:8989/vrmeeting  
All the best

Best regards,
Finovo
"""


   part1 = MIMEText(text, "plain")

   message.attach(part1)

   context = ssl.create_default_context()
   with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
       server.login(sender_email, password)
       server.sendmail(
           sender_email, receiver_email, message.as_string()
       )
