import sqlite3

from core.config import DATABASE, ORDER_ID_START


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            uid TEXT PRIMARY KEY,
            pass_hash TEXT NOT NULL,
            fname TEXT,
            lname TEXT,
            email TEXT,
            address TEXT,
            phno TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS seller (
            sid TEXT PRIMARY KEY,
            sname TEXT,
            pass_hash TEXT NOT NULL,
            address TEXT,
            phno TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS product (
            pid TEXT PRIMARY KEY,
            pname TEXT UNIQUE,
            manufacturer TEXT,
            mfg TEXT,
            exp TEXT,
            price INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            pid TEXT NOT NULL,
            sid TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity >= 0),
            PRIMARY KEY (pid, sid),
            FOREIGN KEY (pid) REFERENCES product (pid) ON DELETE CASCADE,
            FOREIGN KEY (sid) REFERENCES seller (sid) ON DELETE CASCADE
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            oid INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT,
            sid TEXT,
            uid TEXT,
            orderdatetime TEXT DEFAULT (datetime('now', 'localtime')),
            quantity INTEGER,
            price INTEGER,
            FOREIGN KEY (pid) REFERENCES product (pid) ON DELETE CASCADE,
            FOREIGN KEY (sid) REFERENCES seller (sid) ON DELETE CASCADE,
            FOREIGN KEY (uid) REFERENCES customer (uid) ON DELETE CASCADE
        )
    """)

    # making the first order id 1000
    row = conn.execute(
        "SELECT seq FROM sqlite_sequence WHERE name = 'orders'"
    ).fetchone()
    if row is None:
        conn.execute(
            "INSERT INTO sqlite_sequence (name, seq) VALUES ('orders', ?)",
            (ORDER_ID_START - 1,),
        )

    conn.commit()
    conn.close()
