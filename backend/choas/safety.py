# =========================================================
# CHAOSPILOT CHAOS SAFETY
# =========================================================


# Maximum allowed duration for a simulation
MAX_DURATION_SECONDS = 300


# Allowed environments
ALLOWED_ENVIRONMENTS = {
    "development",
    "testing",
    "staging",
    "sandbox"
}


# Production is blocked by default
BLOCKED_ENVIRONMENTS = {
    "production",
    "prod"
}


# =========================================================
# SAFETY RESULT
# =========================================================

def safety_result(
    allowed,
    reason,
    warnings=None
):

    return {
        "allowed": allowed,
        "reason": reason,
        "warnings": warnings or []
    }


# =========================================================
# CHECK ENVIRONMENT
# =========================================================

def check_environment(environment):

    if not environment:

        return safety_result(
            False,
            "Environment is required."
        )


    environment = environment.lower().strip()


    if environment in BLOCKED_ENVIRONMENTS:

        return safety_result(
            False,
            "Chaos experiments are blocked in production."
        )


    if environment not in ALLOWED_ENVIRONMENTS:

        return safety_result(
            False,
            f"Environment '{environment}' is not allowed."
        )


    return safety_result(
        True,
        "Environment is approved for simulation."
    )


# =========================================================
# CHECK DURATION
# =========================================================

def check_duration(duration_seconds):

    if duration_seconds <= 0:

        return safety_result(
            False,
            "Experiment duration must be greater than zero."
        )


    if duration_seconds > MAX_DURATION_SECONDS:

        return safety_result(
            False,
            (
                f"Experiment duration cannot exceed "
                f"{MAX_DURATION_SECONDS} seconds."
            )
        )


    return safety_result(
        True,
        "Experiment duration is within the safe limit."
    )


# =========================================================
# CHECK TARGET
# =========================================================

def check_target(target):

    if not target:

        return safety_result(
            False,
            "Experiment target is required."
        )


    target = target.strip()


    # Prevent obvious dangerous targets
    blocked_targets = {
        "production",
        "prod",
        "live",
        "all",
        "*"
    }


    if target.lower() in blocked_targets:

        return safety_result(
            False,
            "Target is not allowed for chaos simulation."
        )


    return safety_result(
        True,
        "Target is valid."
    )


# =========================================================
# COMPLETE SAFETY CHECK
# =========================================================

def validate_experiment(
    environment,
    duration_seconds,
    target
):

    checks = []


    # Environment
    environment_check = check_environment(
        environment
    )

    checks.append({
        "check": "environment",
        **environment_check
    })


    # Duration
    duration_check = check_duration(
        duration_seconds
    )

    checks.append({
        "check": "duration",
        **duration_check
    })


    # Target
    target_check = check_target(
        target
    )

    checks.append({
        "check": "target",
        **target_check
    })


    # -----------------------------------------------------
    # FINAL DECISION
    # -----------------------------------------------------

    failed_checks = [

        check

        for check in checks

        if not check["allowed"]

    ]


    if failed_checks:

        return {

            "allowed": False,

            "reason":
                failed_checks[0]["reason"],

            "checks":
                checks

        }


    return {

        "allowed": True,

        "reason":
            "All safety checks passed.",

        "checks":
            checks

    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 65)
    print("             CHAOSPILOT SAFETY CHECK")
    print("=" * 65)


    result = validate_experiment(
        environment="development",
        duration_seconds=60,
        target="payment-service"
    )


    print()

    print(
        f"Allowed : {result['allowed']}"
    )

    print(
        f"Reason  : {result['reason']}"
    )


    print("\nChecks:")

    for check in result["checks"]:

        print(
            f"  {check['check']}: "
            f"{check['allowed']} - "
            f"{check['reason']}"
        )


    print()

    print("=" * 65)