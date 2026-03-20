def sendmail(username,
                password,
                smtp_server='smtp.gmail.com',
                smtp_port=587,
                fromEmail=None,
                toEmail=None,
                subject=None,
                body=''):
    
    import smtplib
    from email.mime.text import MIMEText

    import imaplib
    import email

    # Create message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = fromEmail
    msg["To"] = toEmail

    # Connect to SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # secure connection
        server.login(username, password)
        server.send_message(msg)
    return {'From': fromEmail, "To":toEmail, 'Subject': subject }