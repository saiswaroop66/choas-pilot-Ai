from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import uuid4


router = APIRouter(
    prefix="/api/experiments",
    tags=["Chaos Experiments"]
)


# =========================================================
# TEMPORARY STORAGE
# =========================================================

experiments = {}


# =========================================================
# REQUEST MODEL
# =========================================================

class ExperimentCreate(BaseModel):

    application_id: int

    name: str

    description: str = ""

    experiment_type: str

    target: Optional[str] = None

    duration_seconds: int = 60


# =========================================================
# ALLOWED EXPERIMENT TYPES
# =========================================================

ALLOWED_EXPERIMENTS = {
    "latency",
    "service_failure",
    "database_failure",
    "cpu_stress",
    "memory_stress",
    "network_failure"
}


# =========================================================
# CREATE EXPERIMENT
# =========================================================

@router.post("/")
def create_experiment(
    data: ExperimentCreate
):

    if not data.name.strip():

        raise HTTPException(
            status_code=400,
            detail="Experiment name is required."
        )


    experiment_type = (
        data.experiment_type.lower()
    )


    if experiment_type not in ALLOWED_EXPERIMENTS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported experiment type. "
                "Choose from: "
                + ", ".join(
                    sorted(ALLOWED_EXPERIMENTS)
                )
            )
        )


    if data.duration_seconds <= 0:

        raise HTTPException(
            status_code=400,
            detail="Duration must be greater than 0."
        )


    experiment_id = str(
        uuid4()
    )


    experiment = {

        "id":
            experiment_id,

        "application_id":
            data.application_id,

        "name":
            data.name.strip(),

        "description":
            data.description,

        "experiment_type":
            experiment_type,

        "target":
            data.target,

        "duration_seconds":
            data.duration_seconds,

        "status":
            "created",

        "created_at":
            datetime.utcnow().isoformat(),

        "started_at":
            None,

        "completed_at":
            None,

        "result":
            None

    }


    experiments[experiment_id] = (
        experiment
    )


    return {

        "success": True,

        "message":
            "Chaos experiment created.",

        "experiment":
            experiment

    }


# =========================================================
# GET EXPERIMENT
# =========================================================

@router.get("/{experiment_id}")
def get_experiment(
    experiment_id: str
):

    experiment = experiments.get(
        experiment_id
    )


    if not experiment:

        raise HTTPException(
            status_code=404,
            detail="Experiment not found."
        )


    return {

        "success": True,

        "experiment":
            experiment

    }


# =========================================================
# GET APPLICATION EXPERIMENTS
# =========================================================

@router.get(
    "/application/{application_id}"
)
def get_application_experiments(
    application_id: int
):

    results = [

        experiment

        for experiment in experiments.values()

        if experiment["application_id"]
        == application_id

    ]


    return {

        "success": True,

        "application_id":
            application_id,

        "count":
            len(results),

        "experiments":
            results

    }


# =========================================================
# START EXPERIMENT
# =========================================================

@router.post("/{experiment_id}/start")
def start_experiment(
    experiment_id: str
):

    experiment = experiments.get(
        experiment_id
    )


    if not experiment:

        raise HTTPException(
            status_code=404,
            detail="Experiment not found."
        )


    if experiment["status"] == "running":

        raise HTTPException(
            status_code=400,
            detail="Experiment is already running."
        )


    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------
    #
    # This API currently only changes the experiment state.
    # It does NOT actually disrupt a system.
    #
    # Real execution will be implemented later through
    # a controlled chaos engine with explicit safeguards.
    # -----------------------------------------------------

    experiment["status"] = "running"

    experiment["started_at"] = (
        datetime.utcnow().isoformat()
    )


    return {

        "success": True,

        "message":
            "Experiment started in simulation mode.",

        "simulation":
            True,

        "experiment":
            experiment

    }


# =========================================================
# COMPLETE EXPERIMENT
# =========================================================

@router.post("/{experiment_id}/complete")
def complete_experiment(
    experiment_id: str,
    result: Optional[str] = None
):

    experiment = experiments.get(
        experiment_id
    )


    if not experiment:

        raise HTTPException(
            status_code=404,
            detail="Experiment not found."
        )


    experiment["status"] = "completed"

    experiment["completed_at"] = (
        datetime.utcnow().isoformat()
    )

    experiment["result"] = result


    return {

        "success": True,

        "message":
            "Experiment completed.",

        "experiment":
            experiment

    }


# =========================================================
# STOP EXPERIMENT
# =========================================================

@router.post("/{experiment_id}/stop")
def stop_experiment(
    experiment_id: str
):

    experiment = experiments.get(
        experiment_id
    )


    if not experiment:

        raise HTTPException(
            status_code=404,
            detail="Experiment not found."
        )


    experiment["status"] = "stopped"

    experiment["completed_at"] = (
        datetime.utcnow().isoformat()
    )


    return {

        "success": True,

        "message":
            "Experiment stopped.",

        "experiment":
            experiment

    }


# =========================================================
# DELETE EXPERIMENT
# =========================================================

@router.delete("/{experiment_id}")
def delete_experiment(
    experiment_id: str
):

    if experiment_id not in experiments:

        raise HTTPException(
            status_code=404,
            detail="Experiment not found."
        )


    del experiments[
        experiment_id
    ]


    return {

        "success": True,

        "message":
            "Experiment deleted successfully."

    }