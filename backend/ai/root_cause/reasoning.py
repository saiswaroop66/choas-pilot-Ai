import json
from typing import Any, Dict, List, Optional

from ai.llm import get_llm
from ai.root_cause.evidence import EvidenceEngine
from ai.prompts import SYSTEM_PROMPT


# =========================================================
# CHAOSPILOT ROOT CAUSE REASONING ENGINE
# =========================================================


class RootCauseReasoner:

    def __init__(self):

        self.llm = get_llm()

        self.evidence_engine = EvidenceEngine()


    # =====================================================
    # ANALYZE EVIDENCE
    # =====================================================

    def reason(
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
        # COLLECT EVIDENCE
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
        # CONVERT EVIDENCE TO AI CONTEXT
        # -------------------------------------------------

        evidence_context = (
            self.evidence_engine.to_ai_context()
        )


        # -------------------------------------------------
        # BUILD REASONING PROMPT
        # -------------------------------------------------

        prompt = f"""
You are the root-cause reasoning engine of ChaosPilot.

Your task is to determine the most likely technical
root cause of a software failure.

You MUST reason from the supplied evidence.

Do not invent:

- files
- functions
- line numbers
- dependencies
- logs
- errors
- system behavior

Separate:

1. Observed facts
2. Reasoning
3. Hypothesis
4. Confidence

Use stronger evidence before weaker evidence.

A stack trace pointing to an exact line is stronger
than a general project structure observation.

A log occurring immediately before the failure is
strong evidence.

A chaos experiment that reproduces the failure should
increase confidence in the corresponding hypothesis.

FAILURE:

{failure}


RANKED EVIDENCE:

{evidence_context}


PROJECT MAP:

{project_map or "No project map available."}


CHAOS RESULT:

{chaos_result or "No chaos result available."}


Determine:

1. Most likely root cause
2. Exact failure location
3. Evidence supporting the conclusion
4. How the failure propagated
5. Alternative possible causes
6. Confidence from 0 to 1
7. What should be investigated next

Return ONLY valid JSON:

{{
    "summary": "...",
    "root_cause": "...",
    "confidence": 0.0,

    "failure_location": {{
        "file": "...",
        "function": "...",
        "line": 0
    }},

    "observed_facts": [
        "..."
    ],

    "reasoning": [
        "..."
    ],

    "evidence": [
        "..."
    ],

    "failure_propagation": [
        "..."
    ],

    "alternative_causes": [
        "..."
    ],

    "next_investigation": [
        "..."
    ]
}}
"""


        # -------------------------------------------------
        # CALL GROQ
        # -------------------------------------------------

        response = self.llm.generate(

            system_prompt=SYSTEM_PROMPT,

            user_prompt=prompt,

            temperature=0.1,

            max_tokens=3500

        )


        # -------------------------------------------------
        # PARSE RESPONSE
        # -------------------------------------------------

        result = self._parse_response(
            response
        )


        # -------------------------------------------------
        # RETURN
        # -------------------------------------------------

        return {

            "success": True,

            "analysis": result,

            "evidence_count":
                len(evidence),

            "evidence_summary":
                self.evidence_engine.build_summary()

        }


    # =====================================================
    # PARSE RESPONSE
    # =====================================================

    def _parse_response(
        self,
        response: str
    ) -> Dict[str, Any]:

        if not response:

            return self._empty_result()


        cleaned = response.strip()


        # -------------------------------------------------
        # REMOVE MARKDOWN JSON
        # -------------------------------------------------

        if cleaned.startswith(
            "```json"
        ):

            cleaned = cleaned[7:]


        elif cleaned.startswith(
            "```"
        ):

            cleaned = cleaned[3:]


        if cleaned.endswith(
            "```"
        ):

            cleaned = cleaned[:-3]


        cleaned = cleaned.strip()


        # -------------------------------------------------
        # PARSE JSON
        # -------------------------------------------------

        try:

            result = json.loads(
                cleaned
            )

        except json.JSONDecodeError:

            return {

                "summary":
                    "Groq returned a non-JSON response.",

                "root_cause":
                    cleaned,

                "confidence":
                    0,

                "failure_location":
                    {},

                "observed_facts":
                    [],

                "reasoning":
                    [],

                "evidence":
                    [],

                "failure_propagation":
                    [],

                "alternative_causes":
                    [],

                "next_investigation":
                    []

            }


        return self._normalize(
            result
        )


    # =====================================================
    # NORMALIZE RESULT
    # =====================================================

    def _normalize(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        confidence = result.get(
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


        confidence = max(
            0,
            min(
                1,
                confidence
            )
        )


        location = result.get(
            "failure_location",
            {}
        )


        if not isinstance(
            location,
            dict
        ):

            location = {}


        return {

            "summary":
                result.get(
                    "summary",
                    ""
                ),

            "root_cause":
                result.get(
                    "root_cause"
                ),

            "confidence":
                confidence,

            "failure_location": {

                "file":
                    location.get(
                        "file"
                    ),

                "function":
                    location.get(
                        "function"
                    ),

                "line":
                    location.get(
                        "line"
                    )

            },

            "observed_facts":
                self._ensure_list(
                    result.get(
                        "observed_facts",
                        []
                    )
                ),

            "reasoning":
                self._ensure_list(
                    result.get(
                        "reasoning",
                        []
                    )
                ),

            "evidence":
                self._ensure_list(
                    result.get(
                        "evidence",
                        []
                    )
                ),

            "failure_propagation":
                self._ensure_list(
                    result.get(
                        "failure_propagation",
                        []
                    )
                ),

            "alternative_causes":
                self._ensure_list(
                    result.get(
                        "alternative_causes",
                        []
                    )
                ),

            "next_investigation":
                self._ensure_list(
                    result.get(
                        "next_investigation",
                        []
                    )
                )

        }


    # =====================================================
    # ENSURE LIST
    # =====================================================

    def _ensure_list(
        self,
        value: Any
    ) -> List[Any]:

        if value is None:

            return []


        if isinstance(
            value,
            list
        ):

            return value


        return [value]


    # =====================================================
    # EMPTY RESULT
    # =====================================================

    def _empty_result(self):

        return {

            "summary":
                "No reasoning result available.",

            "root_cause":
                None,

            "confidence":
                0,

            "failure_location": {},

            "observed_facts":
                [],

            "reasoning":
                [],

            "evidence":
                [],

            "failure_propagation":
                [],

            "alternative_causes":
                [],

            "next_investigation":
                []

        }


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

    reasoner = RootCauseReasoner()

    return reasoner.reason(

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
    print("          CHAOSPILOT ROOT CAUSE REASONER")
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

            "payment.py"

        ],

        "functions": [

            "connect_database",

            "process_payment"

        ]

    }


    logs = [

        "ERROR Database connection timeout",

        "ERROR Connection pool exhausted",

        "ERROR Payment request failed"

    ]


    stack_trace = (
        'File "database.py", '
        'line 42, '
        'in connect_database'
    )


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

        reasoner = RootCauseReasoner()


        result = reasoner.reason(

            failure=failure,

            project_map=project_map,

            logs=logs,

            stack_trace=stack_trace,

            chaos_result=chaos_result,

            dependencies=dependencies,

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
            "Reasoning test failed:"
        )

        print(
            error
        )


    print()
    print("=" * 70)