from pathlib import Path


# =========================================================
# CHAOSPILOT FILE ANALYZER
# =========================================================

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".go",
    ".rs",
    ".html",
    ".css",
    ".json",
    ".yaml",
    ".yml",
    ".sql",
}


# =========================================================
# READ FILE
# =========================================================

def read_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            "Provided path is not a file."
        )

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {file_path.suffix}"
        )

    file_size = file_path.stat().st_size

    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            "File is too large to analyze."
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
# ANALYZE FILE
# =========================================================

def analyze_file(file_path):

    file_path = Path(file_path)

    content = read_file(
        file_path
    )

    lines = content.splitlines()

    extension = file_path.suffix.lower()

    return {

        "file": str(file_path),

        "name": file_path.name,

        "extension": extension,

        "size": file_path.stat().st_size,

        "line_count": len(lines),

        "empty_lines": sum(
            1
            for line in lines
            if not line.strip()
        ),

        "content": content

    }


# =========================================================
# ANALYZE PROJECT FILES
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

    for file_path in project_path.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if any(
            folder in file_path.parts
            for folder in [
                ".git",
                "__pycache__",
                "node_modules",
                ".venv",
                "venv",
                "env",
                "dist",
                "build"
            ]
        ):
            continue

        try:

            result = analyze_file(
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
# PRINT RESULT
# =========================================================

def print_analysis(results):

    print()

    print("=" * 65)

    print(
        "              CHAOSPILOT FILE ANALYZER"
    )

    print("=" * 65)

    print(
        f"\nFiles analyzed: {len(results)}"
    )

    for result in results:

        print()

        print(
            f"FILE: {result['file']}"
        )

        print("-" * 65)

        if "error" in result:

            print(
                f"ERROR: {result['error']}"
            )

            continue

        print(
            f"Extension   : {result['extension']}"
        )

        print(
            f"Size        : {result['size']} bytes"
        )

        print(
            f"Lines       : {result['line_count']}"
        )

        print(
            f"Empty lines : {result['empty_lines']}"
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

            print_analysis(
                results
            )

        except Exception as error:

            print(
                f"\nFile analyzer error: {error}"
            )