from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import uuid4


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


# =========================================================
# TEMPORARY REPORT STORAGE
# =========================================================

reports = {}


# =========================================================
# REQUEST MODEL
# =========================================================

class ReportCreate(BaseModel):

    application_id: int

    title: str

    summary: str = ""

    root_cause: Optional[str] = None

    severity: Optional[str] = None

    confidence: Optional[float] = None

    affected_files: List[str] = []

    recommendations: List[str] = []

    evidence: List[Dict[str, Any]] = []


# =========================================================
# CREATE REPORT
# =========================================================

@router.post("/")
def create_report(data: ReportCreate):

    if not data.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Report title is required."
        )


    if data.confidence is not None:

        if not 0 <= data.confidence <= 1:

            raise HTTPException(
                status_code=400,
                detail="Confidence must be between 0 and 1."
            )


    report_id = str(
        uuid4()
    )


    report = {

        "id":
            report_id,

        "application_id":
            data.application_id,

        "title":
            data.title.strip(),

        "summary":
            data.summary,

        "root_cause":
            data.root_cause,

        "severity":
            data.severity,

        "confidence":
            data.confidence,

        "affected_files":
            data.affected_files,

        "recommendations":
            data.recommendations,

        "evidence":
            data.evidence,

        "status":
            "generated",

        "created_at":
            datetime.utcnow().isoformat()

    }


    reports[report_id] = report


    return {

        "success": True,

        "message":
            "Report generated successfully.",

        "report":
            report

    }


# =========================================================
# GET REPORT
# =========================================================

@router.get("/{report_id}")
def get_report(report_id: str):

    report = reports.get(
        report_id
    )


    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )


    return {

        "success": True,

        "report":
            report

    }


# =========================================================
# GET APPLICATION REPORTS
# =========================================================

@router.get(
    "/application/{application_id}"
)
def get_application_reports(
    application_id: int
):

    application_reports = [

        report

        for report in reports.values()

        if report["application_id"]
        == application_id

    ]


    return {

        "success": True,

        "application_id":
            application_id,

        "count":
            len(application_reports),

        "reports":
            application_reports

    }


# =========================================================
# UPDATE REPORT
# =========================================================

@router.patch("/{report_id}")
def update_report(
    report_id: str,
    summary: Optional[str] = None,
    root_cause: Optional[str] = None,
    severity: Optional[str] = None,
    confidence: Optional[float] = None
):

    report = reports.get(
        report_id
    )


    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )


    if summary is not None:

        report["summary"] = summary


    if root_cause is not None:

        report["root_cause"] = root_cause


    if severity is not None:

        report["severity"] = severity


    if confidence is not None:

        if not 0 <= confidence <= 1:

            raise HTTPException(
                status_code=400,
                detail="Confidence must be between 0 and 1."
            )

        report["confidence"] = confidence


    report["updated_at"] = (
        datetime.utcnow().isoformat()
    )


    return {

        "success": True,

        "message":
            "Report updated successfully.",

        "report":
            report

    }


# =========================================================
# DELETE REPORT
# =========================================================

@router.delete("/{report_id}")
def delete_report(report_id: str):

    if report_id not in reports:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )


    del reports[
        report_id
    ]


    return {

        "success": True,

        "message":
            "Report deleted successfully."

    }