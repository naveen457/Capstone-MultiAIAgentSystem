import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

DB_PATH = Path(__file__).resolve().parent / "checkpoints.db"

conn = sqlite3.connect(
    str(DB_PATH),
    check_same_thread=False,
)

checkpointer = SqliteSaver(conn)
