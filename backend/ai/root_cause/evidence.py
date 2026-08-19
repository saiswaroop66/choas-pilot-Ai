from typing import Any, Dict, List, Optional


# =========================================================
# CHAOSPILOT EVIDENCE ENGINE
# =========================================================


class EvidenceEngine:

    def __init__(self):
        self.evidence: List[Dict[str, Any]] = []


    # =====================================================
    # COLLECT ALL EVIDENCE
    # =====================================================

    def collect(
        self,
        failure: Optional[Any] = None,
        project_map: Optional[Any] = None,
        logs: Optional[Any] = None,
        stack_trace: Optional[str] = None,
        chaos_result: Optional[Any] = None,
        dependencies: Optional[Any] = None,
        call_graph: Optional[Any] = None
    ) -> List[Dict[str, Any]]:

        self.evidence = []

        # Failure information
        if failure:
            self._add(
                source="failure",
                data=failure,
                confidence=0.95,
                priority="critical"
            )

        # Stack trace
        if stack_trace:
            self._add(
                source="stack_trace",
                data=stack_trace,
                confidence=0.98,
                priority="critical"
            )

        # Logs
        if logs:
            self._add(
                source="logs",
                data=logs,
                confidence=0.90,
                priority="high"
            )

        # Project structure
        if project_map:
            self._add(
                source="project_map",
                data=project_map,
                confidence=0.75,
                priority="medium"
            )

        # Dependencies
        if dependencies:
            self._add(
                source="dependencies",
                data=dependencies,
                confidence=0.80,
                priority="high"
            )

        # Call graph
        if call_graph:
            self._add(
                source="call_graph",
                data=call_graph,
                confidence=0.85,
                priority="high"
            )

        # Chaos experiment
        if chaos_result:
            self._add(
                source="chaos_experiment",
                data=chaos_result,
                confidence=0.92,
                priority="high"
            )

        return self.rank()


    # =====================================================
    # ADD EVIDENCE
    # =====================================================

    def _add(
        self,
        source: str,
        data: Any,
        confidence: float,
        priority: str
    ):

        self.evidence.append({

            "source": source,

            "data": data,

            "confidence": confidence,

            "priority": priority

        })


    # =====================================================
    # RANK EVIDENCE
    # =====================================================

    def rank(self) -> List[Dict[str, Any]]:

        priority_score = {

            "critical": 4,

            "high": 3,

            "medium": 2,

            "low": 1

        }

        self.evidence.sort(

            key=lambda item: (

                priority_score.get(
                    item.get(
                        "priority",
                        "low"
                    ),
                    1
                ),

                item.get(
                    "confidence",
                    0
                )

            ),

            reverse=True

        )

        return self.evidence


    # =====================================================
    # GET STRONG EVIDENCE
    # =====================================================

    def get_strong_evidence(
        self,
        minimum_confidence: float = 0.85
    ) -> List[Dict[str, Any]]:

        return [

            item

            for item in self.evidence

            if item.get(
                "confidence",
                0
            ) >= minimum_confidence

        ]


    # =====================================================
    # GET EVIDENCE BY SOURCE
    # =====================================================

    def get_by_source(
        self,
        source: str
    ) -> List[Dict[str, Any]]:

        return [

            item

            for item in self.evidence

            if item.get(
                "source"
            ) == source

        ]


    # =====================================================
    # EVIDENCE COUNT
    # =====================================================

    def count(self) -> int:

        return len(
            self.evidence
        )


    # =====================================================
    # BUILD AI EVIDENCE SUMMARY
    # =====================================================

    def build_summary(self) -> Dict[str, Any]:

        if not self.evidence:

            return {

                "total": 0,

                "critical": 0,

                "high": 0,

                "medium": 0,

                "low": 0,

                "sources": []

            }


        summary = {

            "total":
                len(self.evidence),

            "critical": 0,

            "high": 0,

            "medium": 0,

            "low": 0,

            "sources": []

        }


        for item in self.evidence:

            priority = item.get(
                "priority",
                "low"
            )

            if priority in summary:

                summary[
                    priority
                ] += 1


            source = item.get(
                "source"
            )

            if source and source not in summary[
                "sources"
            ]:

                summary[
                    "sources"
                ].append(
                    source
                )


        return summary


    # =====================================================
    # CONVERT TO AI CONTEXT
    # =====================================================

    def to_ai_context(self) -> str:

        if not self.evidence:

            return (
                "No evidence was available."
            )


        sections = []


        for index, item in enumerate(
            self.evidence,
            start=1
        ):

            sections.append(

                f"""
EVIDENCE {index}

Source:
{item.get('source')}

Priority:
{item.get('priority')}

Confidence:
{item.get('confidence')}

Data:
{item.get('data')}
""".strip()

            )


        return "\n\n".join(
            sections
        )


# =========================================================
# SIMPLE HELPER
# =========================================================

def collect_evidence(
    failure=None,
    project_map=None,
    logs=None,
    stack_trace=None,
    chaos_result=None,
    dependencies=None,
    call_graph=None
):

    engine = EvidenceEngine()

    return engine.collect(

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
    print("             CHAOSPILOT EVIDENCE ENGINE")
    print("=" * 70)


    engine = EvidenceEngine()


    evidence = engine.collect(

        failure={

            "type":
                "ConnectionError",

            "message":
                "Database connection failed",

            "severity":
                "critical"

        },

        stack_trace=(
            'File "database.py", '
            'line 42, '
            'in connect_database'
        ),

        logs=[

            "ERROR Database timeout",

            "ERROR Connection pool exhausted"

        ],

        project_map={

            "files": [

                "app.py",

                "database.py",

                "payment.py"

            ]

        },

        dependencies=[

            "sqlite3",

            "payment_service"

        ],

        call_graph={

            "process_payment":
                [
                    "connect_database"
                ]

        },

        chaos_result={

            "experiment_type":
                "database_failure",

            "recovered":
                True

        }

    )


    print()

    for item in evidence:

        print(
            f"[{item['priority'].upper()}] "
            f"{item['source']} "
            f"(confidence={item['confidence']})"
        )


    print()

    print("Evidence count:")

    print(
        engine.count()
    )


    print()

    print("Summary:")

    print(
        engine.build_summary()
    )


    print()

    print("AI CONTEXT:")

    print(
        engine.to_ai_context()
    )


    print()

    print("=" * 70)