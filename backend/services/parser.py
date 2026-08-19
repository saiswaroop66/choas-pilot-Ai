import ast
from pathlib import Path


# =========================================================
# CHAOSPILOT CODE PARSER
# =========================================================


def read_source_file(file_path: Path) -> str:
    """
    Read a source file safely.
    """

    try:
        return file_path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )


# =========================================================
# PARSE PYTHON FILE
# =========================================================

def parse_python_file(file_path):
    """
    Parse one Python file and extract:

    - Functions
    - Classes
    - Imports
    - Line numbers
    """

    file_path = Path(file_path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    source_code = read_source_file(
        file_path
    )

    try:

        tree = ast.parse(
            source_code
        )

    except SyntaxError as error:

        return {
            "file": str(file_path),
            "language": "Python",
            "error": "SyntaxError",
            "message": str(error),
            "functions": [],
            "classes": [],
            "imports": []
        }


    functions = []

    classes = []

    imports = []


    # =====================================================
    # ANALYZE AST
    # =====================================================

    for node in ast.walk(tree):

        # -------------------------------------------------
        # FUNCTIONS
        # -------------------------------------------------

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):

            functions.append({

                "name": node.name,

                "line": node.lineno,

                "end_line": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),

                "async": isinstance(
                    node,
                    ast.AsyncFunctionDef
                )

            })


        # -------------------------------------------------
        # CLASSES
        # -------------------------------------------------

        elif isinstance(
            node,
            ast.ClassDef
        ):

            classes.append({

                "name": node.name,

                "line": node.lineno,

                "end_line": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                )

            })


        # -------------------------------------------------
        # NORMAL IMPORT
        # -------------------------------------------------

        elif isinstance(
            node,
            ast.Import
        ):

            for item in node.names:

                imports.append({

                    "name": item.name,

                    "alias": item.asname

                })


        # -------------------------------------------------
        # FROM IMPORT
        # -------------------------------------------------

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            module = node.module or ""

            for item in node.names:

                imports.append({

                    "name": f"{module}.{item.name}",

                    "alias": item.asname

                })


    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "file": str(file_path),

        "language": "Python",

        "functions": functions,

        "classes": classes,

        "imports": imports

    }


# =========================================================
# PARSE PROJECT
# =========================================================

def parse_project(project_path):
    """
    Parse all Python files inside a project.
    """

    project_path = Path(
        project_path
    )

    if not project_path.exists():

        raise FileNotFoundError(
            f"Project path not found: {project_path}"
        )

    if not project_path.is_dir():

        raise ValueError(
            "Project path must be a directory."
        )


    results = []


    for file_path in project_path.rglob(
        "*.py"
    ):

        # Skip virtual environments
        if any(
            folder in file_path.parts
            for folder in [
                ".git",
                "__pycache__",
                "node_modules",
                ".venv",
                "venv",
                "env"
            ]
        ):

            continue


        try:

            result = parse_python_file(
                file_path
            )

            results.append(
                result
            )

        except Exception as error:

            results.append({

                "file": str(file_path),

                "language": "Python",

                "error": "ParserError",

                "message": str(error),

                "functions": [],

                "classes": [],

                "imports": []

            })


    return results


# =========================================================
# PRINT PARSER RESULT
# =========================================================

def print_parser_result(results):

    print()

    print("=" * 65)

    print(
        "                 CHAOSPILOT CODE PARSER"
    )

    print("=" * 65)


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

        print("-" * 65)


        # -------------------------------------------------
        # ERROR
        # -------------------------------------------------

        if "error" in result:

            print(
                f"ERROR: {result['error']}"
            )

            print(
                f"MESSAGE: {result['message']}"
            )

            continue


        # -------------------------------------------------
        # FUNCTIONS
        # -------------------------------------------------

        print("\nFunctions:")


        if result["functions"]:

            for function in result["functions"]:

                function_type = (
                    "async "
                    if function["async"]
                    else ""
                )

                print(
                    f"  {function_type}"
                    f"{function['name']}() "
                    f"[lines "
                    f"{function['line']}-"
                    f"{function['end_line']}]"
                )

        else:

            print(
                "  None"
            )


        # -------------------------------------------------
        # CLASSES
        # -------------------------------------------------

        print("\nClasses:")


        if result["classes"]:

            for class_info in result["classes"]:

                print(
                    f"  {class_info['name']} "
                    f"[lines "
                    f"{class_info['line']}-"
                    f"{class_info['end_line']}]"
                )

        else:

            print(
                "  None"
            )


        # -------------------------------------------------
        # IMPORTS
        # -------------------------------------------------

        print("\nImports:")


        if result["imports"]:

            for import_info in result["imports"]:

                name = import_info["name"]

                alias = import_info["alias"]


                if alias:

                    print(
                        f"  {name} "
                        f"as {alias}"
                    )

                else:

                    print(
                        f"  {name}"
                    )

        else:

            print(
                "  None"
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

            results = parse_project(
                project_path
            )

            print_parser_result(
                results
            )

        except Exception as error:

            print(
                f"\nParser error: {error}"
            )