import json
from typing import Any, Dict, Optional

from ai.llm import get_llm
from ai.prompts import SYSTEM_PROMPT


# =========================================================
# CHAOSPILOT FIX GENERATOR
# =========================================================


class FixGenerator:

    def __init__(self):
        self.llm = get_llm()

    # =====================================================
    # GENERATE FIX
    # =====================================================

    def generate(
        self,
        root_cause: Dict[str, Any],
        impact: Optional[Dict[str, Any]] = None,
        project_map: Optional[Dict[str, Any]] = None,
        evidence: Optional[Any] = None
    ) -> Dict[str, Any]:

        impact = impact or {}
        project_map = project_map or {}

        prompt = f"""
You are the remediation engineer of ChaosPilot.

Generate a practical software-engineering fix for the
confirmed failure.

IMPORTANT RULES:

1. Use ONLY the supplied evidence.
2. Do not invent files or functions.
3. Do not assume a technology that is not present.
4. Prefer the smallest safe fix.
5. Explain WHY the fix solves the root cause.
6. Include implementation steps.
7. Include a code change only when the available
   evidence identifies the affected code clearly.
8. Never recommend disabling security controls,
   authentication, validation, logging, or safety
   mechanisms just to make the error disappear.

ROOT CAUSE:

{json.dumps(root_cause, indent=2, default=str)}

IMPACT:

{json.dumps(impact, indent=2, default=str)}

PROJECT MAP:

{json.dumps(project_map, indent=2, default=str)}

EVIDENCE:

{json.dumps(evidence, indent=2, default=str)}

Return ONLY valid JSON:

{{
    "title": "...",
    "summary": "...",
    "root_cause_addressed": "...",

    "affected_files": [
        "..."
    ],

    "affected_functions": [
        "..."
    ],

    "implementation_steps": [
        "..."
    ],

    "code_changes": [
        {{
            "file": "...",
            "description": "...",
            "before": "...",
            "after": "..."
        }}
    ],

    "configuration_changes": [],

    "dependency_changes": [],

    "risks": [
        "..."
    ],

    "rollback_plan": [
        "..."
    ],

    "verification": [
        "..."
    ],

    "confidence": 0.0
}}
"""

        response = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.1,
            max_tokens=4000
        )

        result = self._parse_response(response)

        return {
            "success": True,
            "fix": result
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

        # Remove Markdown JSON fences
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            result = json.loads(cleaned)

        except json.JSONDecodeError:

            return {
                "title":
                    "AI-generated remediation",

                "summary":
                    cleaned,

                "root_cause_addressed":
                    "",

                "affected_files":
                    [],

                "affected_functions":
                    [],

                "implementation_steps":
                    [],

                "code_changes":
                    [],

                "configuration_changes":
                    [],

                "dependency_changes":
                    [],

                "risks":
                    [],

                "rollback_plan":
                    [],

                "verification":
                    [],

                "confidence":
                    0
            }

        return self._normalize(result)

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
            confidence = float(confidence)

        except (TypeError, ValueError):
            confidence = 0

        confidence = max(
            0,
            min(
                1,
                confidence
            )
        )

        return {
            "title":
                result.get(
                    "title",
                    "Recommended Fix"
                ),

            "summary":
                result.get(
                    "summary",
                    ""
                ),

            "root_cause_addressed":
                result.get(
                    "root_cause_addressed",
                    ""
                ),

            "affected_files":
                self._list(
                    result.get(
                        "affected_files",
                        []
                    )
                ),

            "affected_functions":
                self._list(
                    result.get(
                        "affected_functions",
                        []
                    )
                ),

            "implementation_steps":
                self._list(
                    result.get(
                        "implementation_steps",
                        []
                    )
                ),

            "code_changes":
                self._list(
                    result.get(
                        "code_changes",
                        []
                    )
                ),

            "configuration_changes":
                self._list(
                    result.get(
                        "configuration_changes",
                        []
                    )
                ),

            "dependency_changes":
                self._list(
                    result.get(
                        "dependency_changes",
                        []
                    )
                ),

            "risks":
                self._list(
                    result.get(
                        "risks",
                        []
                    )
                ),

            "rollback_plan":
                self._list(
                    result.get(
                        "rollback_plan",
                        []
                    )
                ),

            "verification":
                self._list(
                    result.get(
                        "verification",
                        []
                    )
                ),

            "confidence":
                confidence
        }

    # =====================================================
    # ENSURE LIST
    # =====================================================

    def _list(
        self,
        value: Any
    ):

        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]

    # =====================================================
    # EMPTY RESULT
    # =====================================================

    def _empty_result(self):

        return {
            "title":
                "No fix generated",

            "summary":
                "The AI did not return a remediation.",

            "root_cause_addressed":
                "",

            "affected_files":
                [],

            "affected_functions":
                [],

            "implementation_steps":
                [],

            "code_changes":
                [],

            "configuration_changes":
                [],

            "dependency_changes":
                [],

            "risks":
                [],

            "rollback_plan":
                [],

            "verification":
                [],

            "confidence":
                0
        }


# =========================================================
# SIMPLE HELPER
# =========================================================


def generate_fix(
    root_cause,
    impact=None,
    project_map=None,
    evidence=None
):

    generator = FixGenerator()

    return generator.generate(

        root_cause=root_cause,

        impact=impact,

        project_map=project_map,

        evidence=evidence

    )


# =========================================================
# TEST
# =========================================================


if __name__ == "__main__":

    root_cause = {

        "root_cause":
            "Database connection pool is exhausted.",

        "confidence":
            0.94,

        "failure_location": {

            "file":
                "database.py",

            "function":
                "connect_database",

            "line":
                42

        }

    }

    impact = {

        "severity":
            "critical",

        "blast_radius":
            "high",

        "affected": {

            "files": [
                "database.py",
                "payment.py"
            ],

            "functions": [
                "connect_database",
                "process_payment"
            ]

        }

    }

    project_map = {

        "files": [
            "app.py",
            "database.py",
            "payment.py"
        ],

        "dependencies": [
            "sqlite3"
        ]

    }

    evidence = [

        {
            "source":
                "stack_trace",

            "data":
                'File "database.py", line 42',

            "confidence":
                0.98
        },

        {
            "source":
                "logs",

            "data":
                "Connection pool exhausted",

            "confidence":
                0.90
        }

    ]

    generator = FixGenerator()

    try:

        result = generator.generate(

            root_cause=root_cause,

            impact=impact,

            project_map=project_map,

            evidence=evidence

        )

        print()
        print("=" * 70)
        print("          CHAOSPILOT FIX GENERATOR")
        print("=" * 70)
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
        print("Fix generation failed:")
        print(error)

    print()
    print("=" * 70)
