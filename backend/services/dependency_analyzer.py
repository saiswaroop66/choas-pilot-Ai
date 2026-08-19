import ast
from pathlib import Path


# =========================================================
# CHAOSPILOT DEPENDENCY ANALYZER
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
# ANALYZE PYTHON FILE
# =========================================================

def analyze_python_dependencies(file_path):

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
        tree = ast.parse(source_code)

    except SyntaxError as error:

        return {
            "file": str(file_path),
            "error": "SyntaxError",
            "message": str(error),
            "dependencies": []
        }


    dependencies = []


    for node in ast.walk(tree):

        # -------------------------------------------------
        # import something
        # -------------------------------------------------

        if isinstance(node, ast.Import):

            for item in node.names:

                dependencies.append({
                    "module": item.name,
                    "type": "external_or_local",
                    "line": node.lineno
                })


        # -------------------------------------------------
        # from something import ...
        # -------------------------------------------------

        elif isinstance(node, ast.ImportFrom):

            module = node.module or ""

            dependencies.append({
                "module": module,
                "type": "external_or_local",
                "line": node.lineno
            })


    # Remove duplicates
    unique_dependencies = []

    seen = set()


    for dependency in dependencies:

        key = (
            dependency["module"],
            dependency["line"]
        )

        if key not in seen:

            seen.add(key)

            unique_dependencies.append(
                dependency
            )


    return {
        "file": str(file_path),
        "language": "Python",
        "dependencies": unique_dependencies
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


    for file_path in project_path.rglob(
        "*.py"
    ):

        if any(
            folder in file_path.parts
            for folder in IGNORED_DIRECTORIES
        ):

            continue


        result = analyze_python_dependencies(
            file_path
        )

        results.append(
            result
        )


    return results


# =========================================================
# PROJECT DEPENDENCY SUMMARY
# =========================================================

def build_dependency_summary(results):

    dependency_map = {}


    for result in results:

        if "error" in result:
            continue


        file_name = result["file"]


        dependency_map[file_name] = [
            dependency["module"]
            for dependency
            in result["dependencies"]
        ]


    return dependency_map


# =========================================================
# PRINT RESULTS
# =========================================================

def print_results(results):

    print()

    print("=" * 70)

    print(
        "             CHAOSPILOT DEPENDENCY ANALYZER"
    )

    print("=" * 70)


    if not results:

        print(
            "\nNo Python files found."
        )

        return


    for result in results:

        print()

        print(
            f"FILE: {result['file']}"
        )

        print("-" * 70)


        if "error" in result:

            print(
                f"ERROR: {result['message']}"
            )

            continue


        dependencies = result["dependencies"]


        if not dependencies:

            print(
                "No dependencies found."
            )

            continue


        for dependency in dependencies:

            print(
                f"  {dependency['module']}"
                f"  → line "
                f"{dependency['line']}"
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

            results = analyze_project(
                project_path
            )

            print_results(
                results
            )

        except Exception as error:

            print(
                f"\nDependency analyzer error: "
                f"{error}"
            )