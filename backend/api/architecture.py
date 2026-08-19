from fastapi import APIRouter, HTTPException
from pathlib import Path

from database.crud import get_application
from services.project_mapper import build_project_map


router = APIRouter(
    prefix="/api/architecture",
    tags=["Architecture"]
)


# =========================================================
# GET APPLICATION ARCHITECTURE
# =========================================================

@router.get("/{application_id}")
def get_architecture(application_id: int):

    # -----------------------------------------------------
    # Find application
    # -----------------------------------------------------

    application = get_application(
        application_id
    )

    if not application:

        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )


    # -----------------------------------------------------
    # Locate uploaded project
    # -----------------------------------------------------

    storage_path = Path(
        __file__
    ).resolve().parent.parent / "storage" / "projects"

    application_directory = (
        storage_path /
        f"application_{application_id}"
    )


    if not application_directory.exists():

        raise HTTPException(
            status_code=404,
            detail="Uploaded project not found."
        )


    # -----------------------------------------------------
    # Find latest project
    # -----------------------------------------------------

    project_directories = [
        directory
        for directory in application_directory.iterdir()
        if directory.is_dir()
    ]


    if not project_directories:

        raise HTTPException(
            status_code=404,
            detail="No project files found."
        )


    latest_project = max(
        project_directories,
        key=lambda directory: directory.stat().st_mtime
    )


    source_directory = (
        latest_project / "source"
    )


    if not source_directory.exists():

        raise HTTPException(
            status_code=404,
            detail="Project source not found."
        )


    # -----------------------------------------------------
    # Build project map
    # -----------------------------------------------------

    try:

        project_map = build_project_map(
            source_directory
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Architecture analysis failed: {error}"
        )


    # -----------------------------------------------------
    # Return architecture
    # -----------------------------------------------------

    return {

        "success": True,

        "application_id":
            application_id,

        "architecture":
            project_map

    }