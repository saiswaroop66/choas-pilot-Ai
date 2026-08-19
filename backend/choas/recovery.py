from datetime import datetime


# =========================================================
# CHAOSPILOT RECOVERY MANAGER
# =========================================================


class RecoveryManager:

    def __init__(self):

        self.recovery_history = []


    # =====================================================
    # VERIFY RECOVERY
    # =====================================================

    def verify_recovery(
        self,
        experiment_result
    ):

        if not experiment_result:

            return {
                "recovered": False,
                "status": "unknown",
                "reason": "No experiment result provided."
            }


        simulation = experiment_result.get(
            "simulation",
            False
        )


        if not simulation:

            return {
                "recovered": False,
                "status": "blocked",
                "reason": (
                    "Only simulation results can "
                    "be verified by this recovery manager."
                )
            }


        recovered = experiment_result.get(
            "recovered",
            False
        )


        if recovered:

            status = "recovered"

            reason = (
                "System successfully returned "
                "to the expected state."
            )

        else:

            status = "recovery_failed"

            reason = (
                "System did not return "
                "to the expected state."
            )


        result = {

            "recovered": recovered,

            "status": status,

            "reason": reason,

            "verified_at":
                datetime.utcnow().isoformat()

        }


        self.recovery_history.append(
            result
        )


        return result


    # =====================================================
    # GENERATE RECOVERY SUMMARY
    # =====================================================

    def generate_summary(
        self,
        experiment_result
    ):

        recovery = self.verify_recovery(
            experiment_result
        )


        impact = experiment_result.get(
            "impact",
            {}
        )


        return {

            "recovery": recovery,

            "impact": {

                "service_available":
                    impact.get(
                        "service_available"
                    ),

                "request_delay":
                    impact.get(
                        "request_delay"
                    ),

                "error_rate":
                    impact.get(
                        "error_rate"
                    )

            },

            "recommendation":
                self._generate_recommendation(
                    recovery,
                    impact
                )

        }


    # =====================================================
    # RECOVERY RECOMMENDATION
    # =====================================================

    def _generate_recommendation(
        self,
        recovery,
        impact
    ):

        if not recovery["recovered"]:

            return (
                "Investigate the affected service "
                "before running another experiment."
            )


        error_rate = impact.get(
            "error_rate",
            0
        )

        request_delay = impact.get(
            "request_delay",
            0
        )


        if error_rate >= 80:

            return (
                "System recovered, but the experiment "
                "caused a significant error rate. "
                "Review service resilience."
            )


        if request_delay >= 500:

            return (
                "System recovered, but significant "
                "latency was observed."
            )


        return (
            "System recovered successfully "
            "with acceptable impact."
        )


# =========================================================
# SIMPLE RECOVERY FUNCTION
# =========================================================

def verify_recovery(
    experiment_result
):

    manager = RecoveryManager()

    return manager.generate_summary(
        experiment_result
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()

    print("=" * 70)

    print(
        "              CHAOSPILOT RECOVERY MANAGER"
    )

    print("=" * 70)


    # Simulated result from chaos engine

    experiment_result = {

        "simulation": True,

        "failure_type":
            "database_failure",

        "recovered":
            True,

        "impact": {

            "service_available":
                False,

            "request_delay":
                0,

            "error_rate":
                80

        }

    }


    result = verify_recovery(
        experiment_result
    )


    print()

    print(
        "Recovery Status:"
    )

    print(
        result["recovery"]["status"]
    )


    print()

    print(
        "Recovered:"
    )

    print(
        result["recovery"]["recovered"]
    )


    print()

    print(
        "Reason:"
    )

    print(
        result["recovery"]["reason"]
    )


    print()

    print(
        "Recommendation:"
    )

    print(
        result["recommendation"]
    )


    print()

    print("=" * 70)