from pathlib import Path

from logs.parser import parse_log_file
from logs.stacktrace import analyze_stack_trace
from services.project_mapper import build_project_map


# =========================================================
# CHAOSPILOT FAILURE CORRELATOR
# =========================================================


def find_matching_file(project_map, file_name):
    """
    Find a project file that matches the file
    mentioned in the stack trace.
    """

    if not file_name:
        return None

    target_name = Path(file_name).name

    for file_info in project_map.get("files", []):

        if file_info["name"] == target_name:
            return file_info

    return None


# =========================================================
# FIND FUNCTION INFORMATION
# =========================================================

def find_function(
    project_map,
    function_name
):

    if not function_name:
        return None

    for file_info in project_map.get(
        "functions",
        []
    ):

        if "error" in file_info:
            continue

        for function in file_info.get(
            "functions",
            []
        ):

            if function["name"] == function_name:

                return {
                    "file": file_info["file"],
                    "function": function
                }

    return None


# =========================================================
# CORRELATE FAILURE
# =========================================================

def correlate_failure(
    project_map,
    stack_trace=None,
    log_result=None
):

    evidence = {

        "failure_detected": False,

        "exception": None,

        "failure_location": None,

        "stack_frames": [],

        "related_logs": [],

        "project_file": None,

        "function": None

    }


    # =====================================================
    # STACK TRACE
    # =====================================================

    if stack_trace:

        stack_result = analyze_stack_trace(
            stack_trace
        )

        evidence["stack_frames"] = (
            stack_result.get(
                "frames",
                []
            )
        )

        evidence["exception"] = (
            stack_result.get(
                "exception"
            )
        )


        root_frame = stack_result.get(
            "root_frame"
        )


        if root_frame:

            evidence["failure_detected"] = True


            evidence["failure_location"] = {

                "file":
                    root_frame["file"],

                "function":
                    root_frame["function"],

                "line":
                    root_frame["line"]

            }


            # -------------------------------------------------
            # Match project file
            # -------------------------------------------------

            project_file = find_matching_file(
                project_map,
                root_frame["file"]
            )

            evidence["project_file"] = (
                project_file
            )


            # -------------------------------------------------
            # Match function
            # -------------------------------------------------

            function_info = find_function(
                project_map,
                root_frame["function"]
            )

            if function_info:

                evidence["function"] = (
                    function_info
                )


    # =====================================================
    # LOGS
    # =====================================================

    if log_result:

        errors = log_result.get(
            "errors",
            []
        )

        evidence["related_logs"] = errors


        if errors:

            evidence["failure_detected"] = True


    return evidence


# =========================================================
# CORRELATE FROM FILES
# =========================================================

def correlate_from_files(
    project_path,
    log_file=None,
    stack_trace=None
):

    print(
        "\nBuilding project map..."
    )

    project_map = build_project_map(
        project_path
    )


    log_result = None


    if log_file:

        log_result = parse_log_file(
            log_file
        )


    evidence = correlate_failure(
        project_map=project_map,
        stack_trace=stack_trace,
        log_result=log_result
    )


    return evidence


# =========================================================
# PRINT EVIDENCE
# =========================================================

def print_evidence(evidence):

    print()

    print("=" * 70)

    print(
        "             CHAOSPILOT FAILURE EVIDENCE"
    )

    print("=" * 70)


    print()

    print(
        f"Failure Detected : "
        f"{evidence['failure_detected']}"
    )


    # =====================================================
    # EXCEPTION
    # =====================================================

    print("\nEXCEPTION")
    print("-" * 70)


    if evidence["exception"]:

        print(
            f"Type    : "
            f"{evidence['exception']['type']}"
        )

        print(
            f"Message : "
            f"{evidence['exception']['message']}"
        )

    else:

        print(
            "No exception detected."
        )


    # =====================================================
    # FAILURE LOCATION
    # =====================================================

    print("\nFAILURE LOCATION")
    print("-" * 70)


    location = evidence.get(
        "failure_location"
    )


    if location:

        print(
            f"File     : {location['file']}"
        )

        print(
            f"Function : {location['function']}"
        )

        print(
            f"Line     : {location['line']}"
        )

    else:

        print(
            "Location not determined."
        )


    # =====================================================
    # PROJECT FILE
    # =====================================================

    print("\nPROJECT MATCH")
    print("-" * 70)


    if evidence["project_file"]:

        print(
            f"Path     : "
            f"{evidence['project_file']['path']}"
        )

        print(
            f"Language : "
            f"{evidence['project_file']['language']}"
        )

    else:

        print(
            "No matching project file found."
        )


    # =====================================================
    # FUNCTION
    # =====================================================

    print("\nFUNCTION ANALYSIS")
    print("-" * 70)


    function_info = evidence.get(
        "function"
    )


    if function_info:

        function = function_info[
            "function"
        ]

        print(
            f"Name      : "
            f"{function['name']}"
        )

        print(
            f"Arguments : "
            f"{function['arguments']}"
        )

        print(
            f"Calls     : "
            f"{function['calls']}"
        )

    else:

        print(
            "Function information not found."
        )


    # =====================================================
    # LOG ERRORS
    # =====================================================

    print("\nRELATED LOG ERRORS")
    print("-" * 70)


    logs = evidence.get(
        "related_logs",
        []
    )


    if not logs:

        print(
            "No related log errors."
        )

    else:

        for log in logs:

            print(
                f"[Line {log['line_number']}] "
                f"{log['message']}"
            )


    print()

    print("=" * 70)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    project_path = input(
        "Enter project source path: "
    ).strip()


    log_path = input(
        "Enter log file path (optional): "
    ).strip()


    print(
        "\nPaste stack trace."
    )

    print(
        "Type END when finished."
    )

    print()


    trace_lines = []


    while True:

        line = input()

        if line == "END":
            break

        trace_lines.append(
            line
        )


    stack_trace = "\n".join(
        trace_lines
    )


    try:

        evidence = correlate_from_files(
            project_path=project_path,
            log_file=log_path
            if log_path
            else None,
            stack_trace=stack_trace
        )


        print_evidence(
            evidence
        )


    except Exception as error:

        print(
            f"\nCorrelation error: {error}"
        )