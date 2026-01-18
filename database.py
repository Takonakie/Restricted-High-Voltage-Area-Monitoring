import sqlite3
from datetime import datetime

# Database file name
DB_NAME = "stairvision_logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create the table with the 'image_path' column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            details TEXT NOT NULL,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} is ready.")

def log_incident(detail_text, image_path=""): 
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get the current time in a readable format
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert the incident data into the database
    cursor.execute(
        "INSERT INTO incidents (timestamp, details, image_path) VALUES (?, ?, ?)", 
        (current_time, detail_text, image_path)
    )
    
    conn.commit()
    conn.close()
    print(f"[LOG & EVIDENCE] {current_time} - {detail_text}")

if __name__ == "__main__":
    init_db()