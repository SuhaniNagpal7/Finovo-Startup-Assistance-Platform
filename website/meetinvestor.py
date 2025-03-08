import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def meetinvestor(emil):
   sender_email = "examplemsit@gmail.com"
   receiver_email = "suhaninagpal634@gmail.com"
   password = "smwtujbcmobbmbda"

   message = MIMEMultipart("alternative")
   message["Subject"] = "Thanks for registering as an Startup on finovo"
   message["From"] = sender_email
   message["To"] = receiver_email


   text = """

Dear Founder,

Thank you for expressing your interest in investing one of the enlisted startup on our website it is our great honour to have you onboard to the virtual meet on http://localhost:8989/vrmeeting  
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
