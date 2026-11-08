import json
import sqlite3
import time
from typing import Any, Dict, Optional
from storage.database import DB_PATH, init_db


class RunRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        init_db(self.db_path)

    def save_run(self, run_result: Any) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO runs (run_id, task, status, output, error, steps_taken, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_result.run_id,
                run_result.trace.task,
                run_result.status,
                str(run_result.output) if run_result.output is not None else None,
                run_result.error,
                run_result.steps_taken,
                time.time(),
            ),
        )

        for event in run_result.trace.events:
            cursor.execute(
                """
                INSERT OR REPLACE INTO trace_events (event_id, run_id, step, event_type, payload, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.run_id,
                    event.step,
                    event.event_type,
                    json.dumps(event.payload),
                    event.timestamp,
                ),
            )

        conn.commit()
        conn.close()