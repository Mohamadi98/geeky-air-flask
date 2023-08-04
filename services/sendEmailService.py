import yagmail

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        yag = yagmail.SMTP(sender_email, sender_password)
        yag.send(to=recipient_email, subject=subject, contents=body)
        return "Email sent successfully!"
    except Exception as e:
        return f'there was an error: {e}'