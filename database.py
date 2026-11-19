"""Small helper module for the SQLite prediction-history database."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "predictions.db"

def create_table():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                total_sqft REAL NOT NULL,
                bhk INTEGER NOT NULL,
                bathrooms REAL NOT NULL,
                predicted_price_lakh REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

if __name__ == "__main__":
    create_table()
    print(f"Database ready: {DB_PATH}")
