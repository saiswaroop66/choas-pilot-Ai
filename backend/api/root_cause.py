from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4


router = APIRouter(
    prefix="/api/root-cause",
    tags=["Root Cause Analysis"]
)


# =========================================================
# TEMPORARY STORAGE
# =========================================================

analyses = {}


# =========================================================
# REQUEST MODEL
# =========================================================

class RootCauseRequest(BaseModel):

    application_id: int

    failure_id: Optional[str] = None

    error_type: Optional[str] = None

    error_message: Optional[str] = None

    file: Optional[str] = None

    function: Optional[str] = None

    line: Optional[int] = None


# =========================================================
# CREATE ROOT-CAUSE ANALYSIS
# =========================================================

@router.post("/")
def create_root_cause_analysis(
    data: RootCauseRequest
):

    analysis_id = str(uuid4())


    analysis = {

        "id": analysis_id,

        "application_id":
            data.application_id,

        "failure_id":
            data.failure_id,

        "status":
            "pending",

        "error": {

            "type":
                data.error_type,

            "message":
                data.error_message

        },

        "location": {

            "file":
                data.file,

            "function":
                data.function,

            "line":
                data.line

        },

        "root_cause":
            None,

        "evidence":
            [],

        "impact":
            None,

        "recommendation":
            None,

        "confidence":
            None,

        "created_at":
            datetime.utcnow().isoformat()

    }


    analyses[analysis_id] = analysis


    return {

        "success": True,

        "message":
            "Root-cause analysis created.",

        "analysis":
            analysis

    }


# =========================================================
# GET ANALYSIS
# =========================================================

@router.get("/{analysis_id}")
def get_root_cause_analysis(
    analysis_id: str
):

    analysis = analyses.get(
        analysis_id
    )


    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Root-cause analysis not found."
        )


    return {

        "success": True,

        "analysis":
            analysis

    }


# =========================================================
# GET APPLICATION ANALYSES
# =========================================================

@router.get(
    "/application/{application_id}"
)
def get_application_analyses(
    application_id: int
):

    results = [

        analysis

        for analysis in analyses.values()

        if analysis["application_id"]
        == application_id

    ]


    return {

        "success": True,

        "application_id":
            application_id,

        "count":
            len(results),

        "analyses":
            results

    }


# =========================================================
# UPDATE ANALYSIS RESULT
# =========================================================

@router.patch("/{analysis_id}")
def update_root_cause_analysis(
    analysis_id: str,
    root_cause: Optional[str] = None,
    impact: Optional[str] = None,
    recommendation: Optional[str] = None,
    confidence: Optional[float] = None,
    status: str = "completed"
):

    analysis = analyses.get(
        analysis_id
    )


    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Root-cause analysis not found."
        )


    if root_cause is not None:

        analysis["root_cause"] = root_cause


    if impact is not None:

        analysis["impact"] = impact


    if recommendation is not None:

        analysis["recommendation"] = (
            recommendation
        )


    if confidence is not None:

        if not 0 <= confidence <= 1:

            raise HTTPException(
                status_code=400,
                detail="Confidence must be between 0 and 1."
            )

        analysis["confidence"] = confidence


    analysis["status"] = status


    analysis["updated_at"] = (
        datetime.utcnow().isoformat()
    )


    return {

        "success": True,

        "message":
            "Root-cause analysis updated.",

        "analysis":
            analysis

    }