import re
from pathlib import Path
from datetime import datetime


# =========================================================
# CHAOSPILOT LOG PARSER
# =========================================================

LOG_LEVELS = {
    "DEBUG",
    "INFO",
    "WARNING",
    "WARN",
    "ERROR",
    "CRITICAL",
    "FATAL"
}


# =========================================================
# PARSE TIMESTAMP
# =========================================================

def parse_timestamp(value):

    if not value:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S,%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f"
    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt
            ).isoformat()

        except ValueError:
            continue

    return value


# =========================================================
# PARSE LOG LINE
# =========================================================

def parse_log_line(line, line_number):

    line = line.strip()

    if not line:
        return None


    # -----------------------------------------------------
    # Timestamp
    # -----------------------------------------------------

    timestamp = None

    timestamp_match = re.search(
        r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[,.]\d+)?)",
        line
    )

    if timestamp_match:

        timestamp = parse_timestamp(
            timestamp_match.group(1)
        )


    # -----------------------------------------------------
    # Log level
    # -----------------------------------------------------

    level = "UNKNOWN"

    level_match = re.search(
        r"\b(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\b",
        line,
        re.IGNORECASE
    )

    if level_match:

        level = level_match.group(1).upper()

        if level == "WARN":
            level = "WARNING"


    # -----------------------------------------------------
    # Message
    # -----------------------------------------------------

    message = line

    if level_match:

        message = line[
            level_match.end():
        ].strip()

    return {
        "line_number": line_number,
        "timestamp": timestamp,
        "level": level,
        "message": message,
        "raw": line
    }


# =========================================================
# EXTRACT EXCEPTION
# =========================================================

def extract_exception(message):

    patterns = [
        r"([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception))",
        r"([A-Za-z_][A-Za-z0-9_]*Error)",
        r"([A-Za-z_][A-Za-z0-9_]*Exception)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            message
        )

        if match:

            return match.group(1)

    return None


# =========================================================
# PARSE LOG FILE
# =========================================================

def parse_log_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"Log file not found: {file_path}"
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


    events = []

    errors = []

    warnings = []


    for line_number, line in enumerate(
        content.splitlines(),
        start=1
    ):

        event = parse_log_line(
            line,
            line_number
        )

        if not event:
            continue


        exception = extract_exception(
            event["message"]
        )

        event["exception"] = exception


        events.append(event)


        if event["level"] in {
            "ERROR",
            "CRITICAL",
            "FATAL"
        }:

            errors.append(event)


        elif event["level"] == "WARNING":

            warnings.append(event)


    return {

        "file": str(file_path),

        "total_events": len(events),

        "error_count": len(errors),

        "warning_count": len(warnings),

        "events": events,

        "errors": errors,

        "warnings": warnings

    }


# =========================================================
# PRINT RESULTS
# =========================================================

def print_results(result):

    print()

    print("=" * 70)

    print(
        "                 CHAOSPILOT LOG PARSER"
    )

    print("=" * 70)

    print()

    print(
        f"File          : {result['file']}"
    )

    print(
        f"Total Events  : {result['total_events']}"
    )

    print(
        f"Errors        : {result['error_count']}"
    )

    print(
        f"Warnings      : {result['warning_count']}"
    )


    print("\nERROR EVENTS")
    print("-" * 70)


    if not result["errors"]:

        print("No errors found.")

    else:

        for event in result["errors"]:

            print(
                f"[Line {event['line_number']}] "
                f"{event['level']} "
                f"{event['message']}"
            )

            if event["exception"]:

                print(
                    f"  Exception: "
                    f"{event['exception']}"
                )


    print("\nWARNING EVENTS")
    print("-" * 70)


    if not result["warnings"]:

        print("No warnings found.")

    else:

        for event in result["warnings"]:

            print(
                f"[Line {event['line_number']}] "
                f"{event['message']}"
            )


    print()

    print("=" * 70)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    log_path = input(
        "Enter log file path: "
    ).strip()


    if not log_path:

        print(
            "\nLog path cannot be empty."
        )

    else:

        try:

            result = parse_log_file(
                log_path
            )

            print_results(
                result
            )

        except Exception as error:

            print(
                f"\nLog parser error: {error}"
            )