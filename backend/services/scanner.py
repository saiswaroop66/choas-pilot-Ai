from pathlib import Path


# =========================================================
# CHAOSPILOT CODEBASE SCANNER
# =========================================================

IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".vscode",
    ".idea",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
}


SUPPORTED_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "React JSX",
    ".ts": "TypeScript",
    ".tsx": "React TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".go": "Go",
    ".rs": "Rust",
    ".html": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".sql": "SQL",
}


# =========================================================
# CHECK IGNORED PATH
# =========================================================

def is_ignored(path: Path) -> bool:

    return any(
        part in IGNORED_DIRECTORIES
        for part in path.parts
    )


# =========================================================
# SCAN PROJECT
# =========================================================

def scan_project(project_path):

    project_path = Path(project_path)

    if not project_path.exists():

        raise FileNotFoundError(
            f"Project path does not exist: {project_path}"
        )

    if not project_path.is_dir():

        raise ValueError(
            "Project path must be a directory."
        )


    files = []

    total_files = 0

    supported_files = 0

    total_size = 0


    for file_path in project_path.rglob("*"):

        if file_path.is_dir():
            continue

        if is_ignored(file_path):
            continue


        total_files += 1


        try:

            file_size = file_path.stat().st_size

        except OSError:

            continue


        total_size += file_size


        extension = file_path.suffix.lower()

        language = SUPPORTED_EXTENSIONS.get(
            extension
        )


        if not language:
            continue


        supported_files += 1


        relative_path = file_path.relative_to(
            project_path
        )


        files.append({

            "name": file_path.name,

            "path": str(relative_path),

            "extension": extension,

            "language": language,

            "size": file_size

        })


    # =====================================================
    # LANGUAGE STATISTICS
    # =====================================================

    languages = {}

    for file in files:

        language = file["language"]

        languages[language] = (
            languages.get(language, 0) + 1
        )


    # =====================================================
    # RESULT
    # =====================================================

    return {

        "project_path": str(project_path),

        "total_files": total_files,

        "supported_files": supported_files,

        "total_size": total_size,

        "languages": languages,

        "files": files

    }


# =========================================================
# PRINT SCAN RESULT
# =========================================================

def print_scan_result(result):

    print("\n")
    print("=" * 60)
    print("          CHAOSPILOT CODEBASE SCANNER")
    print("=" * 60)

    print(
        f"Project       : {result['project_path']}"
    )

    print(
        f"Total files   : {result['total_files']}"
    )

    print(
        f"Supported     : {result['supported_files']}"
    )

    print(
        f"Total size    : {result['total_size']} bytes"
    )


    print("\nLanguages")
    print("-" * 60)


    for language, count in result["languages"].items():

        print(
            f"{language:<25} {count} file(s)"
        )


    print("\nFiles")
    print("-" * 60)


    for file in result["files"]:

        print(
            f"{file['language']:<20} "
            f"{file['path']}"
        )


    print("=" * 60)


# =========================================================
# TEST SCANNER
# =========================================================

if __name__ == "__main__":

    project_path = input(
        "Enter project source path: "
    ).strip()


    try:

        result = scan_project(
            project_path
        )

        print_scan_result(
            result
        )

    except Exception as error:

        print(
            f"\nScanner error: {error}"
        )