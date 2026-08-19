from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from database.crud import (
    create_application,
    get_application,
    get_user_applications,
    delete_application
)
from services.application_service import save_project_zip


router = APIRouter(
    prefix="/api/applications",
    tags=["Applications"]
)


# =========================================================
# CREATE APPLICATION + UPLOAD PROJECT
# =========================================================

@router.post("/upload")
async def add_application(
    user_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    environment: str = Form("development"),
    project: UploadFile = File(...)
):

    if not name.strip():

        raise HTTPException(
            status_code=400,
            detail="Application name is required."
        )

    if not project.filename:

        raise HTTPException(
            status_code=400,
            detail="Project ZIP file is required."
        )

    if not project.filename.lower().endswith(".zip"):

        raise HTTPException(
            status_code=400,
            detail="Only ZIP project files are supported."
        )

    # Create application in database
    application_id = create_application(
        user_id=user_id,
        name=name,
        description=description,
        repository="",
        environment=environment
    )

    # Save and extract project
    project_info = save_project_zip(
        application_id,
        project
    )

    return {
        "success": True,
        "message": "Application and project uploaded successfully.",
        "application_id": application_id,
        "project": project_info
    }


# =========================================================
# GET SINGLE APPLICATION
# =========================================================

@router.get("/{application_id}")
def get_single_application(application_id: int):

    application = get_application(application_id)

    if not application:

        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    return {
        "success": True,
        "application": dict(application)
    }


# =========================================================
# GET USER APPLICATIONS
# =========================================================

@router.get("/user/{user_id}")
def get_applications(user_id: int):

    applications = get_user_applications(user_id)

    return {
        "success": True,
        "count": len(applications),
        "applications": [
            dict(application)
            for application in applications
        ]
    }


# =========================================================
# DELETE APPLICATION
# =========================================================

@router.delete("/{application_id}")
def remove_application(application_id: int):

    application = get_application(application_id)

    if not application:

        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    delete_application(application_id)

    return {
        "success": True,
        "message": "Application deleted successfully."
    }