from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


# =========================================================
# CHAOSPILOT EXPERIMENT MODEL
# =========================================================

@dataclass
class Experiment:

    application_id: int

    name: str

    experiment_type: str

    target: str

    environment: str

    duration_seconds: int = 60

    description: str = ""

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    status: str = "created"

    created_at: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    started_at: Optional[str] = None

    completed_at: Optional[str] = None

    result: Optional[dict] = None


# =========================================================
# CREATE EXPERIMENT
# =========================================================

def create_experiment(
    application_id: int,
    name: str,
    experiment_type: str,
    target: str,
    environment: str,
    duration_seconds: int = 60,
    description: str = ""
):

    return Experiment(

        application_id=application_id,

        name=name,

        experiment_type=experiment_type,

        target=target,

        environment=environment,

        duration_seconds=duration_seconds,

        description=description

    )


# =========================================================
# START EXPERIMENT
# =========================================================

def start_experiment(experiment: Experiment):

    if experiment.status == "running":

        raise ValueError(
            "Experiment is already running."
        )


    if experiment.status == "completed":

        raise ValueError(
            "Completed experiments cannot be restarted."
        )


    experiment.status = "running"

    experiment.started_at = (
        datetime.utcnow().isoformat()
    )


    return experiment


# =========================================================
# COMPLETE EXPERIMENT
# =========================================================

def complete_experiment(
    experiment: Experiment,
    result: Optional[dict] = None
):

    experiment.status = "completed"

    experiment.completed_at = (
        datetime.utcnow().isoformat()
    )

    experiment.result = result


    return experiment


# =========================================================
# STOP EXPERIMENT
# =========================================================

def stop_experiment(
    experiment: Experiment
):

    experiment.status = "stopped"

    experiment.completed_at = (
        datetime.utcnow().isoformat()
    )


    return experiment


# =========================================================
# CONVERT TO DICTIONARY
# =========================================================

def experiment_to_dict(
    experiment: Experiment
):

    return {

        "id":
            experiment.id,

        "application_id":
            experiment.application_id,

        "name":
            experiment.name,

        "experiment_type":
            experiment.experiment_type,

        "target":
            experiment.target,

        "environment":
            experiment.environment,

        "duration_seconds":
            experiment.duration_seconds,

        "description":
            experiment.description,

        "status":
            experiment.status,

        "created_at":
            experiment.created_at,

        "started_at":
            experiment.started_at,

        "completed_at":
            experiment.completed_at,

        "result":
            experiment.result

    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 65)
    print("          CHAOSPILOT EXPERIMENT MANAGER")
    print("=" * 65)


    experiment = create_experiment(

        application_id=1,

        name="Database Latency Test",

        experiment_type="latency",

        target="database-service",

        environment="development",

        duration_seconds=30,

        description=(
            "Simulate database latency "
            "and observe application behavior."
        )

    )


    print("\nCreated:")
    print(
        experiment_to_dict(
            experiment
        )
    )


    start_experiment(
        experiment
    )


    print("\nAfter Start:")
    print(
        experiment_to_dict(
            experiment
        )
    )


    complete_experiment(

        experiment,

        result={
            "simulation": True,
            "impact": "Low",
            "recovered": True
        }

    )


    print("\nAfter Completion:")
    print(
        experiment_to_dict(
            experiment
        )
    )


    print()
    print("=" * 65)