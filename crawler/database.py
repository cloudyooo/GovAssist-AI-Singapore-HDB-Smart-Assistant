import sqlite3
import os

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

DB_PATH = "database/knowledge.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        title TEXT,
        url TEXT UNIQUE,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database created successfully.")


def save_page(source, title, url, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO knowledge
    (source, title, url, content)
    VALUES (?, ?, ?, ?)
    """, (source, title, url, content))

    conn.commit()
    conn.close()


def count_pages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM knowledge")
    total = cursor.fetchone()[0]

    conn.close()

    return total


if __name__ == "__main__":
    create_database()
    print(f"Total pages stored: {count_pages()}")