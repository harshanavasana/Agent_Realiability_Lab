import sqlite3

DB_PATH = "arl_runs.db"


def init_db(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            output TEXT,
            error TEXT,
            steps_taken INTEGER NOT NULL,
            created_at REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trace_events (
            event_id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            step INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            timestamp REAL NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkpoints (
            checkpoint_id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            step INTEGER NOT NULL,
            state TEXT NOT NULL,
            output TEXT,
            timestamp REAL NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
    """)

    conn.commit()
    conn.close()