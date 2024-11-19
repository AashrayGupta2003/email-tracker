from flask import Flask, request, send_file, jsonify, render_template
import sqlite3
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Function to log email open events
def log_open_event(email_id, sequence_id, ip, user_agent):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emails
        SET opened = 1, opened_timestamp = ?, ip_address = ?, user_agent = ?
        WHERE email_id = ? AND sequence_id = ?
    """, (datetime.datetime.now(), ip, user_agent, email_id, sequence_id))
    conn.commit()
    conn.close()

# Function to send email with tracking pixel
# def send_html_email(email_id, sequence_id, recipient_email, plain_text_content):
#     sender_email = "chandrayaan2iit@gmail.com"
#     subject = "HTML Email Example with Tracking"
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     password = "mjvv ogzx hfzj tsqy"  # Use app-specific password for Gmail

#     msg = MIMEMultipart('mixed')
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = subject

#     # Tracking pixel URL with email_id and sequence_id
#     # tracking_pixel_url = f"http://localhost:5000/track_pixel/{email_id}/{sequence_id}"
#     tracking_pixel_url = f"https://raw.githubusercontent.com/AashrayGupta2003/email-tracker/refs/heads/main/sample_img.jpeg"

#     # HTML content with embedded tracking pixel
#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Email with Tracking Pixel</title>
#     </head>
#     <body>
#         <p>{plain_text_content}</p> <!-- Display the plain text content in the body -->
#         <img src="{tracking_pixel_url}" width="100" height="100" style="display:none;">
#     </body>
#     </html>
#     """

#     # msg.attach(MIMEText(plain_text_content, 'plain'))
#     msg.attach(MIMEText(html_content, 'html'))

#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()  # Secure the connection
#         server.login(sender_email, password)
#         server.sendmail(sender_email, recipient_email, msg.as_string())
#     print("Email sent successfully!")

# def send_html_email(email_id, sequence_id, recipient_email, plain_text_content):
#     sender_email = "chandrayaan2iit@gmail.com"
#     subject = "HTML Email Example with Tracking"
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     password = "mjvv ogzx hfzj tsqy"  # Use app-specific password for Gmail

#     msg = MIMEMultipart('mixed')
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = subject

#     # Hidden form for tracking
#     tracking_form = f'''
#     <html>
#         <body>
#             <form id="trackingForm" method="POST" action="http://localhost:5000/track_open/{email_id}/{sequence_id}">
#                 <input type="hidden" name="tracking" value="1">
#             </form>
#             <script>
#                 document.getElementById('trackingForm').submit();
#             </script>
#             <p>{plain_text_content}</p>
#         </body>
#     </html>
#     '''

#     msg.attach(MIMEText(tracking_form, 'html'))

#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()  # Secure the connection
#         server.login(sender_email, password)
#         server.sendmail(sender_email, recipient_email, msg.as_string())
#     print("Email sent successfully!")

def send_html_email(email_id, sequence_id, recipient_email, plain_text_content):
    sender_email = "chandrayaan2iit@gmail.com"
    subject = "Your Netflix Membership Has Been Suspended"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    password = "mjvv ogzx hfzj tsqy"  # Use app-specific password for Gmail 

    msg = MIMEMultipart('mixed')
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Netflix-style email content with a suspension message
    tracking_form = f'''
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #141414; color: #fff; margin: 0; padding: 0;">
            <div style="text-align: center; padding: 40px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" alt="Netflix Logo" style="width: 200px; margin-bottom: 20px;">
                
                <h1 style="font-size: 32px; font-weight: bold; color: #e50914;">Hello,</h1>
                
                <p style="font-size: 18px; line-height: 1.6; color: #fff; margin-bottom: 30px;">
                    We're sorry to inform you that your Netflix account has been temporarily suspended due to an issue with your payment details.
                </p>
                <p style="font-size: 18px; line-height: 1.6; color: #fff; margin-bottom: 30px;">
                    To continue enjoying your favorite shows and movies, click the button below to resolve the issue and resume your membership.
                </p>
                
                <!-- Flashy Submit Button -->
                <form id="trackingForm" method="POST" action="http://localhost:5000/track_open/{email_id}/{sequence_id}">
                    <button type="submit" style="background-color: #e50914; color: white; font-size: 24px; font-weight: bold; padding: 20px 40px; border-radius: 5px; border: none; cursor: pointer; transition: background-color 0.3s, transform 0.2s;">
                        Resume Membership
                    </button>
                </form>
                
                <!-- Flashy button hover effect -->
                <style>
                    button:hover {{
                        background-color: #f40612;
                        transform: scale(1.05);
                    }}
                    button:focus {{
                        outline: none;
                    }}
                </style>
            </div>

            <footer style="text-align: center; padding: 20px; background-color: #333; color: #999; font-size: 14px;">
                <p>Netflix, Inc. | 100 Winchester Circle, Los Gatos, CA 95032</p>
            </footer>
        </body>
    </html>
    '''

    msg.attach(MIMEText(tracking_form, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")

# Route to serve index.html
@app.route("/")
def home():
    return render_template("index.html")

# # Route to log email opens
# @app.route("/track_pixel/<email_id>/<sequence_id>")
# def track_pixel(email_id, sequence_id):
#     ip = request.remote_addr
#     user_agent = request.headers.get("User-Agent")
    
#     log_open_event(email_id, sequence_id, ip, user_agent)
    
#     # return send_file("1x1_pixel.png", mimetype="image/png")
#     return send_file("sample_img.jpeg", mimetype="image/png")

@app.route("/track_open/<email_id>/<sequence_id>", methods=["GET", "POST"])
def track_open(email_id, sequence_id):
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    
    # Log open event to database
    log_open_event(email_id, sequence_id, ip, user_agent)
    
    # Return a simple 204 response (empty response with no content)
    return '', 204  # No content, since we're just logging the open event via form submission


# Route to handle email sending
@app.route("/send_email", methods=["GET", "POST"])
def send_email():
    if request.method == "GET":
        return render_template("send_email.html")
    
    data = request.json
    recipient = data.get("recipient")
    content = data.get("content")  # Get the email text content from the request

    # Assign email_id as the recipient’s email address
    email_id = recipient
    
    # Check if this email_id already exists and get the latest sequence_id
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(sequence_id) FROM emails WHERE email_id = ?", (email_id,))
    result = cursor.fetchone()
    sequence_id = (result[0] + 1) if result[0] is not None else 1  # Increment if exists, else start at 1

    # Log email in database
    cursor.execute("""
        INSERT INTO emails (email_id, sequence_id, recipient, sent_timestamp, opened)
        VALUES (?, ?, ?, ?, 0)
    """, (email_id, sequence_id, recipient, datetime.datetime.now()))
    conn.commit()
    conn.close()
    
    # Send email with tracking pixel
    send_html_email(email_id, sequence_id, recipient, content)  # Pass content as plain text message
    
    return jsonify({"status": "email sent", "email_id": email_id, "sequence_id": sequence_id})

# Route to get list of emails and metadata

@app.route("/emails")
def get_emails():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT email_id, sequence_id, recipient, sent_timestamp, opened, opened_timestamp, ip_address, user_agent
        FROM emails
    """)
    emails = cursor.fetchall()
    conn.close()

    # Pass the data to the template
    return render_template("email_dashboard.html", emails=emails)


# @app.route("/emails")
# def get_emails():
#     conn = sqlite3.connect("emails.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT email_id, sequence_id, recipient, sent_timestamp, opened, opened_timestamp, ip_address, user_agent
#         FROM emails
#     """)
#     emails = cursor.fetchall()
#     conn.close()
    
#     email_list = [
#         {
#             "email_id": row[0],
#             "sequence_id": row[1],
#             "recipient": row[2],
#             "sent_timestamp": row[3],
#             "opened": bool(row[4]),
#             "opened_timestamp": row[5],
#             "ip_address": row[6],
#             "user_agent": row[7]
#         }
#         for row in emails
#     ]
    
#     return jsonify(email_list)

    
if __name__ == "__main__":
    app.run(debug=True)
