import json
from typing import Any, Dict, Optional

from ai.llm import get_llm
from ai.prompts import SYSTEM_PROMPT


# =========================================================
# CHAOSPILOT TEST GENERATOR
# =========================================================


class TestGenerator:

    def __init__(self):
        self.llm = get_llm()

    # =====================================================
    # GENERATE TESTS
    # =====================================================

    def generate(
        self,
        root_cause: Dict[str, Any],
        fix: Optional[Dict[str, Any]] = None,
        impact: Optional[Dict[str, Any]] = None,
        project_map: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        fix = fix or {}
        impact = impact or {}
        project_map = project_map or {}

        prompt = f"""
You are the software testing engineer of ChaosPilot.

Generate tests that verify whether the proposed fix
actually resolves the detected failure.

Use ONLY the supplied project evidence.

Do not invent files, functions, APIs, frameworks,
dependencies, or test commands.

ROOT CAUSE:

{json.dumps(root_cause, indent=2, default=str)}

PROPOSED FIX:

{json.dumps(fix, indent=2, default=str)}

IMPACT:

{json.dumps(impact, indent=2, default=str)}

PROJECT MAP:

{json.dumps(project_map, indent=2, default=str)}

Generate:

1. Unit tests
2. Integration tests
3. Failure-recovery tests
4. Regression tests
5. Chaos/resilience tests when appropriate

For every test provide:

- test name
- purpose
- type
- target file/function
- setup
- steps
- expected result
- priority

Return ONLY valid JSON:

{{
    "summary": "...",

    "tests": [
        {{
            "name": "...",
            "type": "unit",
            "purpose": "...",
            "target_file": "...",
            "target_function": "...",
            "setup": [],
            "steps": [],
            "expected_result": "...",
            "priority": "high"
        }}
    ],

    "regression_tests": [],

    "resilience_tests": [],

    "verification_strategy": [],

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
            "tests": result
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
                "summary":
                    "AI returned a non-JSON test plan.",

                "tests": [],

                "regression_tests": [],

                "resilience_tests": [],

                "verification_strategy": [],

                "confidence": 0
            }

        return self._normalize(result)

    # =====================================================
    # NORMALIZE
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

            "summary":
                result.get(
                    "summary",
                    ""
                ),

            "tests":
                self._ensure_list(
                    result.get(
                        "tests",
                        []
                    )
                ),

            "regression_tests":
                self._ensure_list(
                    result.get(
                        "regression_tests",
                        []
                    )
                ),

            "resilience_tests":
                self._ensure_list(
                    result.get(
                        "resilience_tests",
                        []
                    )
                ),

            "verification_strategy":
                self._ensure_list(
                    result.get(
                        "verification_strategy",
                        []
                    )
                ),

            "confidence":
                confidence
        }

    # =====================================================
    # ENSURE LIST
    # =====================================================

    def _ensure_list(
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

            "summary":
                "No tests generated.",

            "tests": [],

            "regression_tests": [],

            "resilience_tests": [],

            "verification_strategy": [],

            "confidence":
                0
        }


# =========================================================
# SIMPLE HELPER
# =========================================================


def generate_tests(
    root_cause,
    fix=None,
    impact=None,
    project_map=None
):

    generator = TestGenerator()

    return generator.generate(

        root_cause=root_cause,

        fix=fix,

        impact=impact,

        project_map=project_map

    )


# =========================================================
# TEST
# =========================================================


if __name__ == "__main__":

    root_cause = {

        "root_cause":
            "Database connection pool exhaustion",

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

    fix = {

        "title":
            "Improve database connection handling",

        "summary":
            "Ensure database connections are released correctly.",

        "affected_files": [
            "database.py"
        ],

        "affected_functions": [
            "connect_database"
        ]

    }

    impact = {

        "severity":
            "critical",

        "blast_radius":
            "high"

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

    generator = TestGenerator()

    try:

        result = generator.generate(

            root_cause=root_cause,

            fix=fix,

            impact=impact,

            project_map=project_map

        )

        print()

        print("=" * 70)

        print(
            "             CHAOSPILOT TEST GENERATOR"
        )

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

        print(
            "Test generation failed:"
        )

        print(
            error
        )

    print()

    print("=" * 70)
