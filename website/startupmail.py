import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def startupmail(email):
   sender_email = "examplemsit@gmail.com"
   receiver_email = email
   password = "smwtujbcmobbmbda"

   message = MIMEMultipart("alternative")
   message["Subject"] = "Thanks for registering as an Startup on finovo"
   message["From"] = sender_email
   message["To"] = receiver_email


   text = """

Dear Founder,

Thank you for expressing your interest in registering your startup on our website. We are excited to have you on board and showcase your company to our community of users. To ensure authenticity and maintain the credibility of our platform, we kindly request you to provide us with the necessary government documents for verification purposes.

These documents are essential for us to confirm the legitimacy and existence of your startup. The information you provide will be handled with utmost confidentiality and used solely for verification purposes. Rest assured that we follow strict security measures to protect your data.

Please share the following government documents with us:

Company registration certificate
Tax identification number (TIN)
Any relevant licenses or permits
Once we have verified the provided documents, we will proceed with enlisting your startup on our website. This verification process is crucial to maintain the trust and reliability of our platform for all users.

We appreciate your understanding and cooperation in this matter. Should you have any questions or require further assistance, please feel free to reach out to us. We look forward to showcasing your startup on our website and supporting your journey.

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
