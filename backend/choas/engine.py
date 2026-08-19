from datetime import datetime
import time

from chaos.failure_types import (
    get_failure_type,
    is_supported_failure
)

from chaos.safety import (
    validate_experiment
)

from chaos.experiments import (
    Experiment,
    start_experiment,
    complete_experiment,
    stop_experiment,
    experiment_to_dict
)


# =========================================================
# CHAOSPILOT CHAOS ENGINE
# =========================================================


class ChaosEngine:

    def __init__(self):

        self.running_experiments = {}


    # =====================================================
    # VALIDATE EXPERIMENT
    # =====================================================

    def validate(self, experiment: Experiment):

        # Check failure type
        if not is_supported_failure(
            experiment.experiment_type
        ):

            return {
                "allowed": False,
                "reason": (
                    f"Unsupported failure type: "
                    f"{experiment.experiment_type}"
                )
            }


        # Check safety rules
        safety = validate_experiment(

            environment=
                experiment.environment,

            duration_seconds=
                experiment.duration_seconds,

            target=
                experiment.target

        )


        return safety


    # =====================================================
    # START SIMULATION
    # =====================================================

    def run_simulation(
        self,
        experiment: Experiment
    ):

        # -------------------------------------------------
        # SAFETY CHECK
        # -------------------------------------------------

        validation = self.validate(
            experiment
        )


        if not validation["allowed"]:

            return {

                "success": False,

                "status": "blocked",

                "reason":
                    validation["reason"],

                "experiment":
                    experiment_to_dict(
                        experiment
                    )

            }


        # -------------------------------------------------
        # FAILURE INFORMATION
        # -------------------------------------------------

        failure = get_failure_type(
            experiment.experiment_type
        )


        # -------------------------------------------------
        # START
        # -------------------------------------------------

        try:

            start_experiment(
                experiment
            )

        except ValueError as error:

            return {

                "success": False,

                "status": "error",

                "reason": str(error)

            }


        self.running_experiments[
            experiment.id
        ] = experiment


        # -------------------------------------------------
        # SIMULATION
        # -------------------------------------------------

        started_at = (
            datetime.utcnow().isoformat()
        )


        simulation_result = {

            "simulation": True,

            "failure_type":
                experiment.experiment_type,

            "failure_name":
                failure["name"],

            "category":
                failure["category"],

            "target":
                experiment.target,

            "started_at":
                started_at,

            "observations": [],

            "impact": {

                "service_available":
                    True,

                "request_delay":
                    0,

                "error_rate":
                    0

            },

            "recovery_required":
                True

        }


        # -------------------------------------------------
        # SIMULATED OBSERVATION
        # -------------------------------------------------

        if experiment.experiment_type == "latency":

            simulation_result[
                "observations"
            ].append(
                "Simulated network latency."
            )

            simulation_result[
                "impact"
            ]["request_delay"] = 500


        elif experiment.experiment_type == "service_failure":

            simulation_result[
                "observations"
            ].append(
                "Simulated service unavailability."
            )

            simulation_result[
                "impact"
            ]["service_available"] = False

            simulation_result[
                "impact"
            ]["error_rate"] = 100


        elif experiment.experiment_type == "database_failure":

            simulation_result[
                "observations"
            ].append(
                "Simulated database connection failure."
            )

            simulation_result[
                "impact"
            ]["service_available"] = False

            simulation_result[
                "impact"
            ]["error_rate"] = 80


        elif experiment.experiment_type == "cpu_stress":

            simulation_result[
                "observations"
            ].append(
                "Simulated high CPU utilization."
            )

            simulation_result[
                "impact"
            ]["request_delay"] = 300


        elif experiment.experiment_type == "memory_stress":

            simulation_result[
                "observations"
            ].append(
                "Simulated high memory utilization."
            )

            simulation_result[
                "impact"
            ]["request_delay"] = 250


        elif experiment.experiment_type == "network_failure":

            simulation_result[
                "observations"
            ].append(
                "Simulated network connectivity loss."
            )

            simulation_result[
                "impact"
            ]["service_available"] = False

            simulation_result[
                "impact"
            ]["error_rate"] = 100


        # -------------------------------------------------
        # COMPLETE SIMULATION
        # -------------------------------------------------

        simulation_result[
            "completed_at"
        ] = datetime.utcnow().isoformat()


        simulation_result[
            "recovered"
        ] = True


        simulation_result[
            "recovery_message"
        ] = (
            "Simulation completed and "
            "system marked as recovered."
        )


        complete_experiment(

            experiment,

            simulation_result

        )


        self.running_experiments.pop(
            experiment.id,
            None
        )


        return {

            "success": True,

            "status":
                "completed",

            "simulation":
                True,

            "experiment":
                experiment_to_dict(
                    experiment
                )

        }


    # =====================================================
    # STOP SIMULATION
    # =====================================================

    def stop(
        self,
        experiment: Experiment
    ):

        if experiment.id not in (
            self.running_experiments
        ):

            return {

                "success": False,

                "message":
                    "Experiment is not running."

            }


        stop_experiment(
            experiment
        )


        self.running_experiments.pop(
            experiment.id,
            None
        )


        return {

            "success": True,

            "status":
                "stopped",

            "experiment":
                experiment_to_dict(
                    experiment
                )

        }


# =========================================================
# SIMPLE TEST
# =========================================================

if __name__ == "__main__":

    print()

    print("=" * 70)

    print(
        "             CHAOSPILOT CHAOS ENGINE"
    )

    print("=" * 70)


    experiment = Experiment(

        application_id=1,

        name="Database Failure Simulation",

        experiment_type="database_failure",

        target="database-service",

        environment="development",

        duration_seconds=30

    )


    engine = ChaosEngine()


    print("\nExperiment:")
    print(
        experiment_to_dict(
            experiment
        )
    )


    print("\nRunning safe simulation...")


    result = engine.run_simulation(
        experiment
    )


    print("\nResult:")

    print(
        result
    )


    print()

    print("=" * 70)
