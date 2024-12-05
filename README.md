# Email Tracker System

## Overview

The Email Tracker System is a Flask-based web application designed to send, track, and log emails. It allows users to send emails, monitor when and where they are opened, and track metadata such as IP address, user agent, and location. The project also provides a clean dashboard to visualize email tracking details. The application uses html emails for more click rate through catchy visuals.

## Features

* Send Emails:

    * Users can send emails via a web interface using a simple form.
    * Emails are sent with a unique tracking link for monitoring.

* Track Email Opens:

    * Tracks when recipients open the email by accessing the tracking URL.
    * Logs metadata such as the recipient's IP address, user agent, location, and time taken to open.

* Dashboard:

    * A dashboard lists all sent emails with details like:
        * Email ID
        * Sequence ID (incremented for every email sent to the same recipient)
        * Recipient Email
        * Timestamp (Sent and Opened)
        * IP Address and Location of the recipient
        * User Agent
        * Time Taken to Open the email.
        
        
## Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.7+
* Flask (`pip install flask`)
* SQLite (built-in with Python)
* Flask-Cors (`pip install flask-cors`)


## Setup Instructions
### Step 1: Clone the Repository

```
git clone <https://github.com/AashrayGupta2003/email-tracker.git>
cd email-tracker 
```

### Step 2: Install Required Python Packages
```
pip install -r requirements.txt
```

### Step 3: Database Setup
1. Create an SQLite database file (`emails.db`):
```
sqlite3 emails.db
```
2. Run the following commands to create the emails table:
```
CREATE TABLE emails (
    sno INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id TEXT,
    sequence_id INTEGER,
    recipient TEXT,
    sent_timestamp TEXT,
    opened INTEGER DEFAULT 0,
    opened_timestamp TEXT,
    ip_address TEXT,
    location TEXT,
    user_agent TEXT,
    time_to_open TEXT
);
```
**OR** \
Run the setup_db.py file using the following command:

```
python3 setup_db.py
```

3. Exit the SQLite CLI:
```
.exit
```

### Step 4: Run the Flask Server
Start the Flask development server:
```
python3 app.py
```
The app will run at `http://0.0.0.0:8080`.

## Project Structure

email-tracker/ \
├── app.py   \
├── static/\
│   &emsp;&emsp;├── css/   \
│   &emsp;&emsp;├── js/                \
├── templates/\
│   &emsp;&emsp;├── index.html\
│   &emsp;&emsp;├── send_email.html\
│   &emsp;&emsp;├── email_dashboard.html\
├── emails.db            \
├── README.md \
├── requirements.txt\
└── .env  \


## How It Works
1. **Sending Emails**:

    * The user inputs the recipient's email and the email content via the send_email.html form.
    * The email is sent using SMTP with a tracking link embedded in the email body.

2. **Tracking Opens**:

    * When the recipient opens the email and clicks on the button, the tracking link is triggered.
    * The server logs the open event along with metadata like IP address, user agent, and location (via an IP geolocation API).
    
3. **Displaying Data**:

    * All email records are stored in the SQLite database.
    * The dashboard (email_dashboard.html) retrieves this data and displays it in a tabular format.
    
## API Endpoints

### 1. Send Email:
* Endpoint: `/send_email`
* Method: `POST`
* Request Body:
```
{
  "recipient": "recipient@example.com",
  "content": "Email content here"
}
```

* Response:
    * `200 OK` on success.
    * `400 Bad Request` for errors.

### 2. Track Open
* **Endpoint**: `/track_open/<email_id>/<sequence_id>`
* **Method**: ``GET``
* **Purpose**: Logs metadata when an email is opened.

### 3. Email Dashboard
* **Endpoint**: `/emails`
* **Method**: `GET`
* **Purpose**: Displays all sent emails with tracking details.

## Dashboard Columns
The dashboard (`email_dashboard.html`) displays the following columns:

1. **S.No.**: Serial number of the sent mail.
2. **Email ID**: Unique identifier for the email.
3. **Sequence ID**: Tracks the number of emails sent to the same recipient.
4. **Recipient**: The email address of the recipient.
5. **Sent Timestamp**: When the email was sent.
6. **Opened**: Whether the email was opened (Yes/No).
7. **Opened Timestamp**: When the email was opened.
8. **IP Address**: The IP address from which the email was opened.
9. **Location**: Geographical location of the IP address.
10. **User Agent**: The browser or device used to open the email.


## Deployment

Using a Cloud VM, Deploy the app to a cloud service (e.g., AWS, Azure) with proper firewall settings to allow traffic on port `8080`. \
This project was deployed on Microsoft Azure.

## Dependencies
* Python 3.7+
* Flask
* SQLite
* SMTP (for sending emails)
* IP Geolocation API (ip-api.com) for location tracking


## License
* This project is licensed under the MIT License. See the `LICENSE` file for more information.