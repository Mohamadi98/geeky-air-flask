from flask import jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Configure the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body))

        # Connect and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return jsonify({
            'message': 'email sent successfuly!'
        })
    
    except Exception as e:
        return f'there was an error: {e}'