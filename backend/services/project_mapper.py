from pathlib import Path

from services.scanner import scan_project
from services.parser import parse_project
from services.function_analyzer import analyze_project as analyze_functions
from services.dependency_analyzer import analyze_project as analyze_dependencies
from services.call_graph import build_call_graph


# =========================================================
# CHAOSPILOT PROJECT MAPPER
# =========================================================


def build_project_map(project_path):
    """
    Build a complete structural map of a project.

    Combines:

    - File information
    - Python structure
    - Functions
    - Dependencies
    - Function call relationships
    """

    project_path = Path(project_path)

    if not project_path.exists():
        raise FileNotFoundError(
            f"Project path not found: {project_path}"
        )

    if not project_path.is_dir():
        raise ValueError(
            "Project path must be a directory."
        )

    # =====================================================
    # 1. SCAN FILES
    # =====================================================

    scan_result = scan_project(
        project_path
    )

    # =====================================================
    # 2. PARSE PYTHON STRUCTURE
    # =====================================================

    parsed_files = parse_project(
        project_path
    )

    # =====================================================
    # 3. ANALYZE FUNCTIONS
    # =====================================================

    function_results = analyze_functions(
        project_path
    )

    # =====================================================
    # 4. ANALYZE DEPENDENCIES
    # =====================================================

    dependency_results = analyze_dependencies(
        project_path
    )

    # =====================================================
    # 5. BUILD CALL GRAPH
    # =====================================================

    call_graph = build_call_graph(
        project_path
    )

    # =====================================================
    # FINAL PROJECT MAP
    # =====================================================

    project_map = {

        "project": {
            "path": str(project_path),

            "total_files":
                scan_result["total_files"],

            "supported_files":
                scan_result["supported_files"],

            "total_size":
                scan_result["total_size"],

            "languages":
                scan_result["languages"]
        },

        "files":
            scan_result["files"],

        "parsed_files":
            parsed_files,

        "functions":
            function_results,

        "dependencies":
            dependency_results,

        "call_graph":
            call_graph
    }

    return project_map


# =========================================================
# PRINT PROJECT MAP SUMMARY
# =========================================================

def print_project_summary(project_map):

    project = project_map["project"]

    print()

    print("=" * 70)

    print(
        "                CHAOSPILOT PROJECT MAP"
    )

    print("=" * 70)

    print()

    print(
        f"Project Path   : {project['path']}"
    )

    print(
        f"Total Files    : {project['total_files']}"
    )

    print(
        f"Supported      : {project['supported_files']}"
    )

    print(
        f"Total Size     : {project['total_size']} bytes"
    )

    print()

    print("Languages")
    print("-" * 70)

    for language, count in project[
        "languages"
    ].items():

        print(
            f"{language:<25} {count} file(s)"
        )

    print()

    print("Python Files")
    print("-" * 70)

    for file_info in project_map[
        "parsed_files"
    ]:

        print(
            file_info["file"]
        )

        if "error" in file_info:

            print(
                f"  ERROR: {file_info['message']}"
            )

            continue

        print(
            f"  Functions: "
            f"{len(file_info['functions'])}"
        )

        print(
            f"  Classes: "
            f"{len(file_info['classes'])}"
        )

        print(
            f"  Imports: "
            f"{len(file_info['imports'])}"
        )

    print()

    print("Function Analysis")
    print("-" * 70)

    total_functions = 0

    for file_info in project_map[
        "functions"
    ]:

        if "error" in file_info:
            continue

        total_functions += len(
            file_info["functions"]
        )

    print(
        f"Total Functions: {total_functions}"
    )

    print()

    print("Dependencies")
    print("-" * 70)

    total_dependencies = 0

    for file_info in project_map[
        "dependencies"
    ]:

        if "error" in file_info:
            continue

        total_dependencies += len(
            file_info["dependencies"]
        )

    print(
        f"Total Dependencies: "
        f"{total_dependencies}"
    )

    print()

    print("Call Graph")
    print("-" * 70)

    total_calls = 0

    for file_info in project_map[
        "call_graph"
    ]:

        if "error" in file_info:
            continue

        for function in file_info[
            "functions"
        ]:

            total_calls += len(
                function["calls"]
            )

    print(
        f"Function Calls: {total_calls}"
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

    if not project_path:

        print(
            "\nProject path cannot be empty."
        )

    else:

        try:

            project_map = build_project_map(
                project_path
            )

            print_project_summary(
                project_map
            )

        except Exception as error:

            print(
                f"\nProject mapper error: "
                f"{error}"
            )