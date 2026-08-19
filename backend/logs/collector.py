from pathlib import Path
from datetime import datetime


# =========================================================
# CHAOSPILOT LOG COLLECTOR
# =========================================================


SUPPORTED_LOG_EXTENSIONS = {
    ".log",
    ".txt"
}


MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB


# =========================================================
# READ LOG FILE
# =========================================================

def read_log_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"Log file not found: {file_path}"
        )

    if not file_path.is_file():

        raise ValueError(
            "Provided path is not a file."
        )

    if file_path.suffix.lower() not in SUPPORTED_LOG_EXTENSIONS:

        raise ValueError(
            "Unsupported log file type."
        )

    file_size = file_path.stat().st_size

    if file_size > MAX_LOG_SIZE:

        raise ValueError(
            "Log file is too large."
        )

    try:

        content = file_path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    return content


# =========================================================
# COLLECT LOG
# =========================================================

def collect_log(file_path):

    file_path = Path(file_path)

    content = read_log_file(
        file_path
    )

    lines = content.splitlines()

    return {

        "file": str(file_path),

        "name": file_path.name,

        "size": file_path.stat().st_size,

        "line_count": len(lines),

        "collected_at":
            datetime.utcnow().isoformat(),

        "content": content

    }


# =========================================================
# COLLECT MULTIPLE LOG FILES
# =========================================================

def collect_logs(log_directory):

    log_directory = Path(
        log_directory
    )

    if not log_directory.exists():

        raise FileNotFoundError(
            f"Log directory not found: {log_directory}"
        )

    results = []


    for file_path in log_directory.rglob("*"):

        if not file_path.is_file():

            continue

        if file_path.suffix.lower() not in SUPPORTED_LOG_EXTENSIONS:

            continue

        try:

            result = collect_log(
                file_path
            )

            results.append(
                result
            )

        except Exception as error:

            results.append({

                "file": str(file_path),

                "error": str(error)

            })


    return results


# =========================================================
# PRINT LOG SUMMARY
# =========================================================

def print_log_summary(logs):

    print()

    print("=" * 65)

    print(
        "                CHAOSPILOT LOG COLLECTOR"
    )

    print("=" * 65)


    print(
        f"\nLogs collected: {len(logs)}"
    )


    for log in logs:

        print()

        print(
            f"FILE: {log['file']}"
        )

        print("-" * 65)


        if "error" in log:

            print(
                f"ERROR: {log['error']}"
            )

            continue


        print(
            f"Size       : {log['size']} bytes"
        )

        print(
            f"Lines      : {log['line_count']}"
        )

        print(
            f"Collected  : {log['collected_at']}"
        )


    print()

    print("=" * 65)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    log_path = input(
        "Enter log file or directory path: "
    ).strip()


    if not log_path:

        print(
            "\nLog path cannot be empty."
        )

    else:

        try:

            path = Path(log_path)


            if path.is_file():

                logs = [
                    collect_log(path)
                ]

            else:

                logs = collect_logs(path)


            print_log_summary(
                logs
            )


        except Exception as error:

            print(
                f"\nLog collector error: "
                f"{error}"
            )
