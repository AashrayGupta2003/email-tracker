import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_email(plain_text_content):
    # Email configuration
    sender_email = "chandrayaan2iit@gmail.com"
    receiver_email = "chandrayaan2iit@gmail.com"  # Change to the recipient's email address
    subject = "HTML Email Example via Gmail"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Port for TLS
    password = "mjvv ogzx hfzj tsqy"  # App-specific password is recommended

    # Creating the email
    msg = MIMEMultipart('mixed')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Tracking Image</title>
    </head>
    <body>
        <img src="https://raw.githubusercontent.com/AashrayGupta2003/email-tracker/refs/heads/main/sample_img.jpeg" alt="test image">
    </body>
    </html>
    """

    # Attach the plain text content and the HTML content
    msg.attach(MIMEText(plain_text_content, 'plain'))  # Attach plain text
    msg.attach(MIMEText(html_content, 'html'))  # Attach HTML content

    # Sending the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Call the function with plain text content
plain_text_message = "This is a plain text version of the email content. If you cannot view HTML, you will see this."
send_html_email(plain_text_message)