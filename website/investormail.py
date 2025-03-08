import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def investormail(email):
   sender_email = "examplemsit@gmail.com"
   receiver_email = email
   password = "smwtujbcmobbmbda"

   message = MIMEMultipart("alternative")
   message["Subject"] = "Thanks for registering as an Investor"
   message["From"] = sender_email
   message["To"] = receiver_email


   text = """

Dear Sir/Ma'am,

Thank you for your interest in registering as an investor on our website. We apologize for the additional steps involved in the registration process, but it is necessary to ensure a nuisance-free experience for all users on our platform.

Please understand that this is a small process, and we aim to make it as quick and efficient as possible. We assure you that we will contact you shortly for the verification procedure.

Thank you for your patience and cooperation. Should you have any further questions or concerns, please don't hesitate to reach out to us.

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
