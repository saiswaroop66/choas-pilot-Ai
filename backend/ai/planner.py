from typing import Any, Dict, List


# =========================================================
# CHAOSPILOT INVESTIGATION PLANNER
# =========================================================


class InvestigationPlanner:

    def __init__(self):
        self.steps = []


    # =====================================================
    # CREATE INVESTIGATION PLAN
    # =====================================================

    def create_plan(
        self,
        failure: Dict[str, Any],
        project_map: Dict[str, Any] | None = None,
        logs: Any = None,
        stack_trace: str | None = None,
        chaos_result: Dict[str, Any] | None = None
    ) -> List[Dict[str, Any]]:

        plan = []

        # -------------------------------------------------
        # STEP 1: UNDERSTAND FAILURE
        # -------------------------------------------------

        plan.append({
            "step": 1,
            "action": "analyze_failure",
            "description": (
                "Identify the error type, message, "
                "severity and affected application."
            ),
            "priority": "high"
        })


        # -------------------------------------------------
        # STEP 2: STACK TRACE
        # -------------------------------------------------

        if stack_trace:

            plan.append({
                "step": 2,
                "action": "analyze_stack_trace",
                "description": (
                    "Trace the failure to the most "
                    "relevant file, function and line."
                ),
                "priority": "critical"
            })


        # -------------------------------------------------
        # STEP 3: PROJECT MAP
        # -------------------------------------------------

        if project_map:

            plan.append({
                "step": 3,
                "action": "analyze_project_map",
                "description": (
                    "Inspect project structure, functions, "
                    "dependencies and call relationships."
                ),
                "priority": "high"
            })


        # -------------------------------------------------
        # STEP 4: LOGS
        # -------------------------------------------------

        if logs:

            plan.append({
                "step": 4,
                "action": "correlate_logs",
                "description": (
                    "Correlate application logs with "
                    "the observed failure."
                ),
                "priority": "high"
            })


        # -------------------------------------------------
        # STEP 5: DEPENDENCIES
        # -------------------------------------------------

        if project_map:

            plan.append({
                "step": 5,
                "action": "trace_dependencies",
                "description": (
                    "Identify dependencies that may "
                    "have contributed to the failure."
                ),
                "priority": "medium"
            })


        # -------------------------------------------------
        # STEP 6: CHAOS RESULT
        # -------------------------------------------------

        if chaos_result:

            plan.append({
                "step": 6,
                "action": "analyze_chaos_result",
                "description": (
                    "Use controlled chaos experiment "
                    "results as additional evidence."
                ),
                "priority": "high"
            })


        # -------------------------------------------------
        # STEP 7: ROOT CAUSE
        # -------------------------------------------------

        plan.append({
            "step": len(plan) + 1,
            "action": "determine_root_cause",
            "description": (
                "Compare all available evidence and "
                "identify the most likely root cause."
            ),
            "priority": "critical"
        })


        # -------------------------------------------------
        # STEP 8: IMPACT
        # -------------------------------------------------

        plan.append({
            "step": len(plan) + 1,
            "action": "determine_impact",
            "description": (
                "Determine affected components and "
                "potential blast radius."
            ),
            "priority": "high"
        })


        # -------------------------------------------------
        # STEP 9: RECOMMENDATION
        # -------------------------------------------------

        plan.append({
            "step": len(plan) + 1,
            "action": "generate_fix",
            "description": (
                "Generate a practical fix and "
                "verification tests."
            ),
            "priority": "high"
        })


        self.steps = plan

        return plan


    # =====================================================
    # GET NEXT STEP
    # =====================================================

    def get_next_step(self):

        if not self.steps:

            return None

        return self.steps[0]


    # =====================================================
    # GET PLAN SUMMARY
    # =====================================================

    def get_summary(self):

        if not self.steps:

            return {
                "total_steps": 0,
                "critical_steps": 0,
                "high_priority_steps": 0
            }


        return {

            "total_steps":
                len(self.steps),

            "critical_steps":
                len([
                    step
                    for step in self.steps
                    if step["priority"] == "critical"
                ]),

            "high_priority_steps":
                len([
                    step
                    for step in self.steps
                    if step["priority"] == "high"
                ])

        }


# =========================================================
# SIMPLE HELPER
# =========================================================

def create_investigation_plan(
    failure,
    project_map=None,
    logs=None,
    stack_trace=None,
    chaos_result=None
):

    planner = InvestigationPlanner()

    return planner.create_plan(

        failure=failure,

        project_map=project_map,

        logs=logs,

        stack_trace=stack_trace,

        chaos_result=chaos_result

    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("          CHAOSPILOT INVESTIGATION PLANNER")
    print("=" * 70)


    failure = {

        "type": "ConnectionError",

        "message":
            "Database connection failed",

        "severity":
            "critical"

    }


    project_map = {

        "files": [
            "app.py",
            "database.py",
            "payment.py"
        ],

        "functions": [
            "connect_database",
            "process_payment"
        ],

        "dependencies": [
            "sqlite3"
        ]

    }


    logs = [

        "ERROR Database connection failed",

        "ERROR Payment request failed"

    ]


    stack_trace = (
        'File "database.py", line 42, '
        'in connect_database'
    )


    chaos_result = {

        "experiment_type":
            "database_failure",

        "recovered":
            True

    }


    planner = InvestigationPlanner()


    plan = planner.create_plan(

        failure=failure,

        project_map=project_map,

        logs=logs,

        stack_trace=stack_trace,

        chaos_result=chaos_result

    )


    print()

    for step in plan:

        print(
            f"{step['step']}. "
            f"{step['action']} "
            f"[{step['priority']}]"
        )

        print(
            f"   {step['description']}"
        )


    print()

    print("Summary:")

    print(
        planner.get_summary()
    )


    print()
    print("=" * 70)