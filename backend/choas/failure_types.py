# =========================================================
# CHAOSPILOT FAILURE TYPES
# =========================================================

FAILURE_TYPES = {
    "latency": {
        "name": "Network Latency",
        "description": (
            "Simulates slow network responses "
            "between services."
        ),
        "category": "network",
        "safe": True
    },

    "service_failure": {
        "name": "Service Failure",
        "description": (
            "Simulates an unavailable application "
            "service."
        ),
        "category": "service",
        "safe": True
    },

    "database_failure": {
        "name": "Database Failure",
        "description": (
            "Simulates a database connection "
            "or availability failure."
        ),
        "category": "database",
        "safe": True
    },

    "cpu_stress": {
        "name": "CPU Stress",
        "description": (
            "Simulates increased CPU utilization."
        ),
        "category": "resource",
        "safe": True
    },

    "memory_stress": {
        "name": "Memory Stress",
        "description": (
            "Simulates increased memory utilization."
        ),
        "category": "resource",
        "safe": True
    },

    "network_failure": {
        "name": "Network Failure",
        "description": (
            "Simulates network connectivity "
            "loss between components."
        ),
        "category": "network",
        "safe": True
    }
}


# =========================================================
# GET FAILURE TYPE
# =========================================================

def get_failure_type(
    failure_type: str
):

    return FAILURE_TYPES.get(
        failure_type
    )


# =========================================================
# CHECK FAILURE TYPE
# =========================================================

def is_supported_failure(
    failure_type: str
):

    return failure_type in FAILURE_TYPES


# =========================================================
# GET ALL FAILURE TYPES
# =========================================================

def get_all_failure_types():

    return list(
        FAILURE_TYPES.keys()
    )


# =========================================================
# GET FAILURE INFORMATION
# =========================================================

def get_failure_information():

    return FAILURE_TYPES


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        CHAOSPILOT FAILURE TYPES")
    print("=" * 60)

    for key, failure in FAILURE_TYPES.items():

        print()
        print(f"Type        : {key}")
        print(f"Name        : {failure['name']}")
        print(f"Category    : {failure['category']}")
        print(f"Safe        : {failure['safe']}")
        print(
            f"Description : "
            f"{failure['description']}"
        )

    print()
    print("=" * 60)