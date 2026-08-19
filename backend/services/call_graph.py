import ast
from pathlib import Path


# =========================================================
# CHAOSPILOT CALL GRAPH
# =========================================================

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
}


# =========================================================
# GET CALLED FUNCTION NAME
# =========================================================

def get_call_name(node):

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    return None


# =========================================================
# ANALYZE FILE
# =========================================================

def analyze_file(file_path):

    file_path = Path(file_path)

    source_code = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    try:
        tree = ast.parse(source_code)

    except SyntaxError as error:

        return {
            "file": str(file_path),
            "error": "SyntaxError",
            "message": str(error),
            "functions": []
        }


    functions = []


    for node in ast.walk(tree):

        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):
            continue


        calls = []


        for child in ast.walk(node):

            if not isinstance(
                child,
                ast.Call
            ):
                continue


            call_name = get_call_name(
                child.func
            )


            if call_name:

                calls.append({
                    "name": call_name,
                    "line": child.lineno
                })


        # Remove duplicate calls
        unique_calls = []

        seen = set()


        for call in calls:

            key = (
                call["name"],
                call["line"]
            )

            if key not in seen:

                seen.add(key)

                unique_calls.append(
                    call
                )


        functions.append({

            "name": node.name,

            "line": node.lineno,

            "end_line": getattr(
                node,
                "end_lineno",
                node.lineno
            ),

            "calls": unique_calls

        })


    return {
        "file": str(file_path),
        "language": "Python",
        "functions": functions
    }


# =========================================================
# BUILD PROJECT CALL GRAPH
# =========================================================

def build_call_graph(project_path):

    project_path = Path(
        project_path
    )

    if not project_path.exists():

        raise FileNotFoundError(
            f"Project path not found: {project_path}"
        )


    graph = []


    for file_path in project_path.rglob(
        "*.py"
    ):

        if any(
            folder in file_path.parts
            for folder in IGNORED_DIRECTORIES
        ):

            continue


        result = analyze_file(
            file_path
        )

        graph.append(
            result
        )


    return graph


# =========================================================
# PRINT CALL GRAPH
# =========================================================

def print_call_graph(graph):

    print()

    print("=" * 70)

    print(
        "               CHAOSPILOT CALL GRAPH"
    )

    print("=" * 70)


    if not graph:

        print(
            "\nNo Python files found."
        )

        return


    for file_info in graph:

        print()

        print(
            f"FILE: {file_info['file']}"
        )

        print("-" * 70)


        if "error" in file_info:

            print(
                f"ERROR: {file_info['message']}"
            )

            continue


        for function in file_info["functions"]:

            print(
                f"\n{function['name']}()"
            )

            print(
                f"  Lines: "
                f"{function['line']}-"
                f"{function['end_line']}"
            )


            if not function["calls"]:

                print(
                    "  Calls: None"
                )

                continue


            print(
                "  Calls:"
            )


            for call in function["calls"]:

                print(
                    f"    → {call['name']}() "
                    f"[line {call['line']}]"
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

            graph = build_call_graph(
                project_path
            )

            print_call_graph(
                graph
            )

        except Exception as error:

            print(
                f"\nCall graph error: {error}"
            )