import sqlite3
from pathlib import Path


# =========================================================
# CHAOSPILOT DATABASE CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = DATA_DIR / "chaospilot.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -------------------------------------------------
        # USERS
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                email TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL,

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                description TEXT,

                environment TEXT DEFAULT 'development',

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
        """)

        # -------------------------------------------------
        # FAILURES
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS failures (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                application_id INTEGER NOT NULL,

                title TEXT NOT NULL,

                description TEXT,

                severity TEXT DEFAULT 'medium',

                error_type TEXT,

                file TEXT,

                function TEXT,

                line INTEGER,

                status TEXT DEFAULT 'open',

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
                    ON DELETE CASCADE

            )
        """)

        # -------------------------------------------------
        # ROOT CAUSE ANALYSES
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS root_cause_analyses (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                application_id INTEGER NOT NULL,

                failure_id INTEGER,

                status TEXT DEFAULT 'pending',

                root_cause TEXT,

                impact TEXT,

                recommendation TEXT,

                confidence REAL,

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at
                    TIMESTAMP,

                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (failure_id)
                    REFERENCES failures(id)
                    ON DELETE SET NULL

            )
        """)

        # -------------------------------------------------
        # EXPERIMENTS
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                application_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                description TEXT,

                experiment_type TEXT NOT NULL,

                target TEXT,

                environment TEXT DEFAULT 'development',

                duration_seconds INTEGER DEFAULT 60,

                status TEXT DEFAULT 'created',

                result TEXT,

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                started_at TIMESTAMP,

                completed_at TIMESTAMP,

                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
                    ON DELETE CASCADE

            )
        """)

        # -------------------------------------------------
        # REPORTS
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                application_id INTEGER NOT NULL,

                title TEXT NOT NULL,

                summary TEXT,

                root_cause TEXT,

                severity TEXT,

                confidence REAL,

                report_data TEXT,

                status TEXT DEFAULT 'generated',

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
                    ON DELETE CASCADE

            )
        """)

        # -------------------------------------------------
        # CHAT HISTORY
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                application_id INTEGER,

                role TEXT NOT NULL,

                message TEXT NOT NULL,

                created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
                    ON DELETE CASCADE

            )
        """)

        connection.commit()

        print(
            "ChaosPilot database initialized successfully."
        )

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# =========================================================
# SIMPLE QUERY HELPER
# =========================================================

def execute_query(
    query,
    parameters=(),
    fetch=False
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            query,
            parameters
        )

        if fetch:

            return cursor.fetchall()

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    init_db()

    print(
        f"Database location:\n{DATABASE_PATH}"
    )