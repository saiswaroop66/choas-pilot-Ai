from pathlib import Path
import shutil
import uuid
import zipfile


# =========================================================
# PROJECT STORAGE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECTS_DIR = BASE_DIR / "storage" / "projects"

PROJECTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SAVE PROJECT ZIP
# =========================================================

def save_project_zip(
    application_id: int,
    uploaded_file
):

    # Create unique project directory
    project_id = str(uuid.uuid4())

    project_dir = (
        PROJECTS_DIR /
        f"application_{application_id}" /
        project_id
    )

    project_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    # Save ZIP
    zip_path = (
        project_dir /
        "project.zip"
    )

    with open(
        zip_path,
        "wb"
    ) as file:

        shutil.copyfileobj(
            uploaded_file.file,
            file
        )


    # Extract ZIP
    extract_dir = (
        project_dir /
        "source"
    )

    extract_dir.mkdir(
        exist_ok=True
    )


    with zipfile.ZipFile(
        zip_path,
        "r"
    ) as zip_file:

        zip_file.extractall(
            extract_dir
        )


    return {
        "project_id": project_id,
        "zip_path": str(zip_path),
        "source_path": str(extract_dir)
    }
