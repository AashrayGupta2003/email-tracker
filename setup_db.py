import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("emails.db")
cursor = conn.cursor()

# Create tables for storing email metadata and tracking events
cursor.execute("""
CREATE TABLE IF NOT EXISTS emails (
    email_id TEXT,  -- Stays the same for each recipient
    sequence_id INTEGER,  -- Unique identifier for each email sent to that recipient
    recipient TEXT,
    sent_timestamp TIMESTAMP,
    opened INTEGER,
    opened_timestamp TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT,
    PRIMARY KEY (email_id, sequence_id)  -- Composite key
)
""")
# cursor.execute("""
# DROP table emails
# """)
conn.commit()
conn.close()
print("Database initialized.")
