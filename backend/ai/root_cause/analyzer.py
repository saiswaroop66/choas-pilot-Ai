from typing import Any, Dict, Optional

from ai.root_cause.detector import FailureDetector
from ai.root_cause.evidence import EvidenceEngine
from ai.root_cause.reasoning import RootCauseReasoner
from ai.root_cause.blast_radius import BlastRadiusAnalyzer


# =========================================================
# CHAOSPILOT ROOT CAUSE ANALYZER
# =========================================================


class RootCauseAnalyzer:

    def __init__(self):

        self.detector = FailureDetector()

        self.evidence_engine = EvidenceEngine()

        self.reasoner = RootCauseReasoner()

        self.blast_radius = BlastRadiusAnalyzer()


    # =====================================================
    # COMPLETE ANALYSIS
    # =====================================================

    def analyze(
        self,
        failure: Dict[str, Any],
        project_map: Optional[Any] = None,
        logs: Optional[Any] = None,
        stack_trace: Optional[str] = None,
        chaos_result: Optional[Any] = None,
        dependencies: Optional[Any] = None,
        call_graph: Optional[Any] = None
    ) -> Dict[str, Any]:

        # -------------------------------------------------
        # STEP 1 — DETECT FAILURE
        # -------------------------------------------------

        detection = self.detector.detect(

            failure=failure,

            logs=logs,

            stack_trace=stack_trace

        )


        # -------------------------------------------------
        # STEP 2 — COLLECT EVIDENCE
        # -------------------------------------------------

        evidence = self.evidence_engine.collect(

            failure=failure,

            project_map=project_map,

            logs=logs,

            stack_trace=stack_trace,

            chaos_result=chaos_result,

            dependencies=dependencies,

            call_graph=call_graph

        )


        # -------------------------------------------------
        # STEP 3 — ROOT CAUSE REASONING
        # -------------------------------------------------

        reasoning = self.reasoner.reason(

            failure=failure,

            project_map=project_map,

            logs=logs,

            stack_trace=stack_trace,

            chaos_result=chaos_result,

            dependencies=dependencies,

            call_graph=call_graph

        )


        # -------------------------------------------------
        # STEP 4 — EXTRACT FAILURE LOCATION
        # -------------------------------------------------

        analysis = reasoning.get(
            "analysis",
            {}
        )

        failure_location = analysis.get(
            "failure_location",
            {}
        )


        if not failure_location:

            failure_location = detection.get(
                "failure_location",
                {}
            )


        # -------------------------------------------------
        # STEP 5 — BLAST RADIUS
        # -------------------------------------------------

        blast_radius = self.blast_radius.analyze(

            failure_location=failure_location,

            project_map=project_map,

            call_graph=call_graph,

            dependencies=dependencies

        )


        # -------------------------------------------------
        # STEP 6 — BUILD FINAL RESULT
        # -------------------------------------------------

        return {

            "success": True,

            "failure_detection": detection,

            "root_cause": analysis,

            "blast_radius": blast_radius,

            "evidence": {

                "items": evidence,

                "count":
                    len(evidence),

                "summary":
                    self.evidence_engine.build_summary()

            },

            "status":
                self._determine_status(
                    analysis
                )

        }


    # =====================================================
    # DETERMINE STATUS
    # =====================================================

    def _determine_status(
        self,
        analysis: Dict[str, Any]
    ) -> str:

        confidence = analysis.get(
            "confidence",
            0
        )

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = 0


        if confidence >= 0.85:

            return "high_confidence"

        if confidence >= 0.60:

            return "moderate_confidence"

        if confidence > 0:

            return "low_confidence"

        return "insufficient_evidence"


# =========================================================
# SIMPLE HELPER
# =========================================================


def analyze_root_cause(
    failure,
    project_map=None,
    logs=None,
    stack_trace=None,
    chaos_result=None,
    dependencies=None,
    call_graph=None
):

    analyzer = RootCauseAnalyzer()

    return analyzer.analyze(

        failure=failure,

        project_map=project_map,

        logs=logs,

        stack_trace=stack_trace,

        chaos_result=chaos_result,

        dependencies=dependencies,

        call_graph=call_graph

    )


# =========================================================
# TEST
# =========================================================


if __name__ == "__main__":

    import json


    print()
    print("=" * 70)
    print("          CHAOSPILOT ROOT CAUSE ANALYZER")
    print("=" * 70)


    failure = {

        "type":
            "ConnectionError",

        "message":
            "Database connection failed",

        "severity":
            "critical"

    }


    project_map = {

        "files": [

            "app.py",

            "database.py",

            "payment.py",

            "orders.py"

        ],

        "functions": [

            "connect_database",

            "process_payment",

            "create_order"

        ],

        "dependencies": [

            "sqlite3",

            "payment_service",

            "order_service"

        ]

    }


    logs = [

        "ERROR Database connection timeout",

        "ERROR Connection pool exhausted",

        "ERROR Payment request failed"

    ]


    stack_trace = """
Traceback (most recent call last):

  File "database.py", line 42, in connect_database

    connection = create_connection()

ConnectionError: Database connection failed
"""


    call_graph = {

        "process_payment": [

            "connect_database"

        ],

        "create_order": [

            "process_payment"

        ]

    }


    chaos_result = {

        "experiment_type":
            "database_failure",

        "recovered":
            True,

        "impact": {

            "error_rate":
                85

        }

    }


    try:

        analyzer = RootCauseAnalyzer()


        result = analyzer.analyze(

            failure=failure,

            project_map=project_map,

            logs=logs,

            stack_trace=stack_trace,

            chaos_result=chaos_result,

            dependencies=[
                "sqlite3",
                "payment_service"
            ],

            call_graph=call_graph

        )


        print()

        print(
            json.dumps(
                result,
                indent=4,
                default=str
            )
        )


    except Exception as error:

        print()

        print(
            "Root cause analysis failed:"
        )

        print(
            error
        )


    print()
    print("=" * 70)
