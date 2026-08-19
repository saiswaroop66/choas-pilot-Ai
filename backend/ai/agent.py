import json
from typing import Any, Dict, Optional

from ai.root_cause.detector import FailureDetector
from ai.root_cause.evidence import EvidenceEngine
from ai.root_cause.reasoning import RootCauseReasoner
from ai.root_cause.blast_radius import BlastRadiusAnalyzer
from ai.impact.analyzer import ImpactAnalyzer
from ai.fixes.generator import FixGenerator
from ai.fixes.validator import FixValidator
from ai.tests.generator import TestGenerator


# =========================================================
# CHAOSPILOT AI AGENT
# =========================================================


class ChaosPilotAgent:

    def __init__(self):

        # Root-cause components
        self.detector = FailureDetector()

        self.evidence_engine = EvidenceEngine()

        self.reasoner = RootCauseReasoner()

        self.blast_radius = BlastRadiusAnalyzer()

        # Impact
        self.impact_analyzer = ImpactAnalyzer()

        # Fixes
        self.fix_generator = FixGenerator()

        self.fix_validator = FixValidator()

        # Tests
        self.test_generator = TestGenerator()


    # =====================================================
    # COMPLETE CHAOSPILOT ANALYSIS
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

        # =================================================
        # STEP 1 — DETECT FAILURE
        # =================================================

        detection = self.detector.detect(

            failure=failure,

            logs=logs,

            stack_trace=stack_trace

        )


        # =================================================
        # STEP 2 — COLLECT EVIDENCE
        # =================================================

        evidence = self.evidence_engine.collect(

            failure=failure,

            project_map=project_map,

            logs=logs,

            stack_trace=stack_trace,

            chaos_result=chaos_result,

            dependencies=dependencies,

            call_graph=call_graph

        )


        # =================================================
        # STEP 3 — ROOT CAUSE REASONING
        # =================================================

        reasoning_result = self.reasoner.reason(

            failure=failure,

            project_map=project_map,

            logs=logs,

            stack_trace=stack_trace,

            chaos_result=chaos_result,

            dependencies=dependencies,

            call_graph=call_graph

        )


        root_cause = reasoning_result.get(
            "analysis",
            {}
        )


        # =================================================
        # STEP 4 — FAILURE LOCATION
        # =================================================

        failure_location = root_cause.get(
            "failure_location",
            {}
        )

        if not failure_location:

            failure_location = detection.get(
                "failure_location",
                {}
            )


        # =================================================
        # STEP 5 — BLAST RADIUS
        # =================================================

        blast_radius = self.blast_radius.analyze(

            failure_location=failure_location,

            project_map=project_map,

            call_graph=call_graph,

            dependencies=dependencies

        )


        # =================================================
        # STEP 6 — IMPACT ANALYSIS
        # =================================================

        impact = self.impact_analyzer.analyze(

            root_cause=root_cause,

            project_map=project_map,

            failure=failure,

            chaos_result=chaos_result

        )


        # =================================================
        # STEP 7 — GENERATE FIX
        # =================================================

        fix_result = self.fix_generator.generate(

            root_cause=root_cause,

            impact=impact,

            project_map=project_map,

            evidence=evidence

        )


        fix = fix_result.get(
            "fix",
            {}
        )


        # =================================================
        # STEP 8 — VALIDATE FIX
        # =================================================

        validation = self.fix_validator.validate(

            fix=fix,

            root_cause=root_cause,

            impact=impact,

            project_map=project_map

        )


        # =================================================
        # STEP 9 — GENERATE TESTS
        # =================================================

        test_result = self.test_generator.generate(

            root_cause=root_cause,

            fix=fix,

            impact=impact,

            project_map=project_map

        )


        tests = test_result.get(
            "tests",
            {}
        )


        # =================================================
        # STEP 10 — FINAL REPORT
        # =================================================

        final_report = self._build_final_report(

            detection=detection,

            evidence=evidence,

            root_cause=root_cause,

            blast_radius=blast_radius,

            impact=impact,

            fix=fix,

            validation=validation,

            tests=tests

        )


        return {

            "success": True,

            "status":
                "completed",

            "report":
                final_report

        }


    # =====================================================
    # FINAL REPORT
    # =====================================================

    def _build_final_report(
        self,
        detection,
        evidence,
        root_cause,
        blast_radius,
        impact,
        fix,
        validation,
        tests
    ):

        return {

            "failure": {

                "type":
                    detection.get(
                        "failure_type"
                    ),

                "exception":
                    detection.get(
                        "exception_type"
                    ),

                "severity":
                    detection.get(
                        "severity"
                    ),

                "location":
                    detection.get(
                        "failure_location",
                        {}
                    )

            },

            "root_cause": {

                "summary":
                    root_cause.get(
                        "summary"
                    ),

                "cause":
                    root_cause.get(
                        "root_cause"
                    ),

                "confidence":
                    root_cause.get(
                        "confidence",
                        0
                    ),

                "reasoning":
                    root_cause.get(
                        "reasoning",
                        []
                    ),

                "evidence":
                    root_cause.get(
                        "evidence",
                        []
                    ),

                "alternative_causes":
                    root_cause.get(
                        "alternative_causes",
                        []
                    )

            },

            "blast_radius":
                blast_radius,

            "impact":
                impact,

            "fix": {

                "generated":
                    bool(fix),

                "details":
                    fix,

                "validation":
                    validation

            },

            "tests": tests,

            "evidence": {

                "count":
                    len(evidence),

                "summary":
                    self.evidence_engine.build_summary()

            }

        }


    # =====================================================
    # ASK CHAOSPILOT
    # =====================================================

    def ask(
        self,
        question: str,
        project_map=None,
        failures=None,
        logs=None,
        root_causes=None,
        chaos_results=None
    ):

        if not question or not question.strip():

            raise ValueError(
                "Question cannot be empty."
            )


        context = {

            "project_map":
                project_map,

            "failures":
                failures,

            "logs":
                logs,

            "root_causes":
                root_causes,

            "chaos_results":
                chaos_results

        }


        # Use the LLM already owned by the reasoning engine.
        llm = self.reasoner.llm


        prompt = f"""
You are ChaosPilot, an AI software resilience engineer.

Answer the developer's question using ONLY the
available application evidence.

APPLICATION CONTEXT:

{json.dumps(context, indent=2, default=str)}

DEVELOPER QUESTION:

{question}

Do not invent information.

Explain the answer clearly and provide practical
engineering guidance.
"""


        response = llm.generate(

            system_prompt=(
                "You are ChaosPilot, an expert "
                "software reliability engineer."
            ),

            user_prompt=prompt,

            temperature=0.2,

            max_tokens=3000

        )


        return {

            "success": True,

            "question":
                question,

            "response":
                response

        }


# =========================================================
# HELPER
# =========================================================


def analyze_failure(
    failure,
    project_map=None,
    logs=None,
    stack_trace=None,
    chaos_result=None,
    dependencies=None,
    call_graph=None
):

    agent = ChaosPilotAgent()

    return agent.analyze(

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

    print()
    print("=" * 70)
    print("              CHAOSPILOT AI AGENT")
    print("=" * 70)
    print()

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

            {
                "name":
                    "connect_database",

                "calls": []

            },

            {
                "name":
                    "process_payment",

                "calls": [
                    "connect_database"
                ]

            }

        ],

        "dependencies": [

            "sqlite3",

            "payment_service"

        ],

        "services": [

            {
                "name":
                    "PaymentService",

                "files": [
                    "payment.py"
                ],

                "functions": [
                    "process_payment"
                ]

            }

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


    dependencies = [

        "sqlite3",

        "payment_service"

    ]


    call_graph = {

        "process_payment": [

            "connect_database"

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

        agent = ChaosPilotAgent()


        result = agent.analyze(

            failure=failure,

            project_map=project_map,

            logs=logs,

            stack_trace=stack_trace,

            chaos_result=chaos_result,

            dependencies=dependencies,

            call_graph=call_graph

        )


        print(
            json.dumps(
                result,
                indent=4,
                default=str
            )
        )


    except Exception as error:

        print()
        print("Agent test failed:")
        print(error)


    print()
    print("=" * 70)