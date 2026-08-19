from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import uuid4


router = APIRouter(
    prefix="/api/failures",
    tags=["Failures"]
)


# =========================================================
# TEMPORARY IN-MEMORY FAILURE STORE
# =========================================================

failures = []


# =========================================================
# REQUEST MODEL
# =========================================================

class FailureCreate(BaseModel):

    application_id: int

    title: str

    description: str = ""

    severity: str = "medium"

    error_type: Optional[str] = None

    file: Optional[str] = None

    function: Optional[str] = None

    line: Optional[int] = None


# =========================================================
# CREATE FAILURE
# =========================================================

@router.post("/")
def create_failure(data: FailureCreate):

    if not data.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Failure title is required."
        )


    allowed_severities = {
        "low",
        "medium",
        "high",
        "critical"
    }


    severity = data.severity.lower()


    if severity not in allowed_severities:

        raise HTTPException(
            status_code=400,
            detail=(
                "Severity must be "
                "low, medium, high, or critical."
            )
        )


    failure = {

        "id": str(uuid4()),

        "application_id":
            data.application_id,

        "title":
            data.title.strip(),

        "description":
            data.description,

        "severity":
            severity,

        "error_type":
            data.error_type,

        "file":
            data.file,

        "function":
            data.function,

        "line":
            data.line,

        "status":
            "open",

        "created_at":
            datetime.utcnow().isoformat()

    }


    failures.append(
        failure
    )


    return {

        "success": True,

        "message":
            "Failure recorded successfully.",

        "failure":
            failure

    }


# =========================================================
# GET APPLICATION FAILURES
# =========================================================

@router.get("/application/{application_id}")
def get_application_failures(
    application_id: int
):

    application_failures = [

        failure

        for failure in failures

        if failure["application_id"]
        == application_id

    ]


    return {

        "success": True,

        "application_id":
            application_id,

        "count":
            len(application_failures),

        "failures":
            application_failures

    }


# =========================================================
# GET SINGLE FAILURE
# =========================================================

@router.get("/{failure_id}")
def get_failure(
    failure_id: str
):

    for failure in failures:

        if failure["id"] == failure_id:

            return {

                "success": True,

                "failure":
                    failure

            }


    raise HTTPException(
        status_code=404,
        detail="Failure not found."
    )


# =========================================================
# UPDATE FAILURE STATUS
# =========================================================

@router.patch("/{failure_id}/status")
def update_failure_status(
    failure_id: str,
    status: str
):

    allowed_statuses = {
        "open",
        "investigating",
        "resolved",
        "ignored"
    }


    if status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. "
                "Use open, investigating, "
                "resolved, or ignored."
            )
        )


    for failure in failures:

        if failure["id"] == failure_id:

            failure["status"] = status

            return {

                "success": True,

                "message":
                    "Failure status updated.",

                "failure":
                    failure

            }


    raise HTTPException(
        status_code=404,
        detail="Failure not found."
    )


# =========================================================
# DELETE FAILURE
# =========================================================

@router.delete("/{failure_id}")
def delete_failure(
    failure_id: str
):

    for index, failure in enumerate(
        failures
    ):

        if failure["id"] == failure_id:

            failures.pop(index)

            return {

                "success": True,

                "message":
                    "Failure deleted successfully."

            }


    raise HTTPException(
        status_code=404,
        detail="Failure not found."
    )