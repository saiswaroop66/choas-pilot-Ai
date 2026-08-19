import ast
from pathlib import Path


# =========================================================
# CHAOSPILOT FUNCTION ANALYZER
# =========================================================


def analyze_function(function_node):
    """
    Analyze a single Python function.
    """

    calls = []

    for node in ast.walk(function_node):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                calls.append(node.func.id)

            elif isinstance(node.func, ast.Attribute):

                calls.append(node.func.attr)


    arguments = []

    for argument in function_node.args.args:

        arguments.append(argument.arg)


    return {
        "name": function_node.name,

        "line": function_node.lineno,

        "end_line": getattr(
            function_node,
            "end_lineno",
            function_node.lineno
        ),

        "arguments": arguments,

        "calls": list(
            dict.fromkeys(calls)
        ),

        "async": isinstance(
            function_node,
            ast.AsyncFunctionDef
        )
    }


# =========================================================
# ANALYZE PYTHON FILE
# =========================================================

def analyze_python_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )


    source_code = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


    try:

        tree = ast.parse(
            source_code
        )

    except SyntaxError as error:

        return {
            "file": str(file_path),
            "error": "SyntaxError",
            "message": str(error),
            "functions": []
        }


    functions = []


    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):

            functions.append(
                analyze_function(node)
            )


    return {
        "file": str(file_path),
        "language": "Python",
        "functions": functions
    }


# =========================================================
# ANALYZE PROJECT
# =========================================================

def analyze_project(project_path):

    project_path = Path(
        project_path
    )

    if not project_path.exists():

        raise FileNotFoundError(
            f"Project path not found: {project_path}"
        )


    results = []


    ignored = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "env",
        "dist",
        "build"
    }


    for file_path in project_path.rglob(
        "*.py"
    ):

        if any(
            folder in file_path.parts
            for folder in ignored
        ):

            continue


        result = analyze_python_file(
            file_path
        )

        results.append(
            result
        )


    return results


# =========================================================
# PRINT RESULTS
# =========================================================

def print_results(results):

    print()

    print("=" * 65)

    print(
        "             CHAOSPILOT FUNCTION ANALYZER"
    )

    print("=" * 65)


    for result in results:

        print()

        print(
            f"FILE: {result['file']}"
        )

        print("-" * 65)


        if "error" in result:

            print(
                f"ERROR: {result['message']}"
            )

            continue


        if not result["functions"]:

            print(
                "No functions found."
            )

            continue


        for function in result["functions"]:

            function_type = (
                "async "
                if function["async"]
                else ""
            )


            print(
                f"\n{function_type}"
                f"{function['name']}()"
            )

            print(
                f"  Lines: "
                f"{function['line']}-"
                f"{function['end_line']}"
            )

            print(
                f"  Arguments: "
                f"{function['arguments']}"
            )

            print(
                f"  Calls: "
                f"{function['calls']}"
            )


    print()

    print("=" * 65)


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

            results = analyze_project(
                project_path
            )

            print_results(
                results
            )

        except Exception as error:

            print(
                f"\nFunction analyzer error: {error}"
            )