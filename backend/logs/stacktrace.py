import re
from pathlib import Path


# =========================================================
# CHAOSPILOT STACK TRACE ANALYZER
# =========================================================


# Example Python stack trace:
#
# Traceback (most recent call last):
#   File "payment.py", line 42, in process_payment
#     result = connect_database()
#   File "database.py", line 18, in connect_database
#     raise ConnectionError("Database unavailable")
# ConnectionError: Database unavailable


FRAME_PATTERN = re.compile(
    r'File ["\'](.+?)["\'], line (\d+), in (.+)'
)


# =========================================================
# EXTRACT STACK FRAMES
# =========================================================

def extract_frames(stack_trace):

    frames = []

    lines = stack_trace.splitlines()

    for line in lines:

        match = FRAME_PATTERN.search(line)

        if not match:
            continue

        file_name = match.group(1)

        line_number = int(
            match.group(2)
        )

        function_name = match.group(3).strip()


        frames.append({

            "file": file_name,

            "line": line_number,

            "function": function_name

        })


    return frames


# =========================================================
# EXTRACT EXCEPTION
# =========================================================

def extract_exception(stack_trace):

    lines = [
        line.strip()
        for line in stack_trace.splitlines()
        if line.strip()
    ]

    if not lines:
        return None


    # Look from bottom because the final line
    # usually contains the actual exception.

    for line in reversed(lines):

        match = re.match(
            r"([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception))"
            r"(?:\s*:\s*(.*))?",
            line
        )

        if match:

            return {

                "type": match.group(1),

                "message":
                    match.group(2) or ""

            }


    return None


# =========================================================
# ANALYZE STACK TRACE
# =========================================================

def analyze_stack_trace(stack_trace):

    if not stack_trace:

        return {

            "valid": False,

            "frames": [],

            "exception": None,

            "root_frame": None

        }


    frames = extract_frames(
        stack_trace
    )

    exception = extract_exception(
        stack_trace
    )


    root_frame = None

    if frames:

        # The final frame is usually closest
        # to where the exception occurred.

        root_frame = frames[-1]


    return {

        "valid": bool(frames),

        "frame_count": len(frames),

        "frames": frames,

        "exception": exception,

        "root_frame": root_frame

    }


# =========================================================
# ANALYZE STACK TRACE FILE
# =========================================================

def analyze_stack_trace_file(
    file_path
):

    file_path = Path(
        file_path
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Stack trace file not found: "
            f"{file_path}"
        )


    stack_trace = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


    return analyze_stack_trace(
        stack_trace
    )


# =========================================================
# PRINT RESULT
# =========================================================

def print_result(result):

    print()

    print("=" * 70)

    print(
        "              CHAOSPILOT STACK TRACE ANALYZER"
    )

    print("=" * 70)


    print()

    print(
        f"Valid Stack Trace : "
        f"{result['valid']}"
    )

    print(
        f"Frames            : "
        f"{result['frame_count']}"
    )


    # -----------------------------------------------------
    # EXCEPTION
    # -----------------------------------------------------

    print("\nEXCEPTION")
    print("-" * 70)


    if result["exception"]:

        print(
            f"Type    : "
            f"{result['exception']['type']}"
        )

        print(
            f"Message : "
            f"{result['exception']['message']}"
        )

    else:

        print(
            "No exception detected."
        )


    # -----------------------------------------------------
    # STACK FRAMES
    # -----------------------------------------------------

    print("\nSTACK FRAMES")
    print("-" * 70)


    if not result["frames"]:

        print(
            "No stack frames detected."
        )

    else:

        for index, frame in enumerate(
            result["frames"],
            start=1
        ):

            print(
                f"{index}. "
                f"{frame['file']}"
            )

            print(
                f"   Function : "
                f"{frame['function']}"
            )

            print(
                f"   Line     : "
                f"{frame['line']}"
            )


    # -----------------------------------------------------
    # ROOT FRAME
    # -----------------------------------------------------

    print("\nLIKELY FAILURE LOCATION")
    print("-" * 70)


    if result["root_frame"]:

        frame = result["root_frame"]

        print(
            f"File     : {frame['file']}"
        )

        print(
            f"Function : {frame['function']}"
        )

        print(
            f"Line     : {frame['line']}"
        )

    else:

        print(
            "Failure location could not be determined."
        )


    print()

    print("=" * 70)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "Paste a Python stack trace."
    )

    print(
        "Type END on a new line when finished."
    )

    print()


    lines = []


    while True:

        line = input()

        if line == "END":

            break

        lines.append(
            line
        )


    stack_trace = "\n".join(
        lines
    )


    result = analyze_stack_trace(
        stack_trace
    )


    print_result(
        result
    )