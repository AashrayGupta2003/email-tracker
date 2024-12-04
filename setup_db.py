import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("emails.db")
cursor = conn.cursor()

# cursor.execute("""
# DROP table emails
# """)

# Create tables for storing email metadata and tracking events
cursor.execute("""
CREATE TABLE IF NOT EXISTS emails (
    sno INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id TEXT,  -- Stays the same for each recipient
    sequence_id INTEGER,  -- Unique identifier for each email sent to that recipient
    recipient TEXT,
    sent_timestamp TIMESTAMP,
    opened INTEGER,
    opened_timestamp TIMESTAMP,
    ip_address TEXT,
    location TEXT,
    user_agent TEXT
    -- PRIMARY KEY (sno, email_id, sequence_id)  -- Composite key
)
""")

conn.commit()
conn.close()
print("Database initialized.")
