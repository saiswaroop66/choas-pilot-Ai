from typing import Any, Dict, List, Optional


# =========================================================
# CHAOSPILOT FIX VALIDATOR
# =========================================================


class FixValidator:

    def __init__(self):
        pass

    # =====================================================
    # VALIDATE FIX
    # =====================================================

    def validate(
        self,
        fix: Dict[str, Any],
        root_cause: Optional[Dict[str, Any]] = None,
        impact: Optional[Dict[str, Any]] = None,
        project_map: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        fix = fix or {}
        root_cause = root_cause or {}
        impact = impact or {}
        project_map = project_map or {}

        checks = []

        # -------------------------------------------------
        # CHECK 1 — FIX EXISTS
        # -------------------------------------------------

        checks.append(
            self._check_fix_exists(fix)
        )

        # -------------------------------------------------
        # CHECK 2 — ROOT CAUSE ALIGNMENT
        # -------------------------------------------------

        checks.append(
            self._check_root_cause_alignment(
                fix,
                root_cause
            )
        )

        # -------------------------------------------------
        # CHECK 3 — FILE VALIDATION
        # -------------------------------------------------

        checks.append(
            self._check_files(
                fix,
                project_map
            )
        )

        # -------------------------------------------------
        # CHECK 4 — FUNCTION VALIDATION
        # -------------------------------------------------

        checks.append(
            self._check_functions(
                fix,
                project_map
            )
        )

        # -------------------------------------------------
        # CHECK 5 — CODE CHANGE SAFETY
        # -------------------------------------------------

        checks.append(
            self._check_code_changes(
                fix
            )
        )

        # -------------------------------------------------
        # CHECK 6 — ROLLBACK PLAN
        # -------------------------------------------------

        checks.append(
            self._check_rollback(
                fix
            )
        )

        # -------------------------------------------------
        # CHECK 7 — VERIFICATION
        # -------------------------------------------------

        checks.append(
            self._check_verification(
                fix
            )
        )

        # -------------------------------------------------
        # CHECK 8 — SECURITY
        # -------------------------------------------------

        checks.append(
            self._check_security(
                fix
            )
        )

        # -------------------------------------------------
        # CALCULATE SCORE
        # -------------------------------------------------

        score = self._calculate_score(
            checks
        )

        status = self._get_status(
            score,
            checks
        )

        warnings = [
            check["message"]
            for check in checks
            if check["severity"] == "warning"
        ]

        errors = [
            check["message"]
            for check in checks
            if check["severity"] == "error"
        ]

        return {

            "success": True,

            "valid":
                status == "approved",

            "status":
                status,

            "score":
                score,

            "checks":
                checks,

            "warnings":
                warnings,

            "errors":
                errors,

            "recommendation":
                self._recommendation(
                    status
                )

        }

    # =====================================================
    # FIX EXISTS
    # =====================================================

    def _check_fix_exists(
        self,
        fix: Dict[str, Any]
    ) -> Dict[str, Any]:

        has_summary = bool(
            fix.get("summary")
        )

        has_steps = bool(
            fix.get("implementation_steps")
        )

        passed = (
            has_summary
            and has_steps
        )

        return {

            "name":
                "fix_completeness",

            "passed":
                passed,

            "severity":
                "info"
                if passed
                else "error",

            "message":
                "Fix contains a summary and implementation steps."
                if passed
                else "Generated fix is incomplete."

        }

    # =====================================================
    # ROOT CAUSE ALIGNMENT
    # =====================================================

    def _check_root_cause_alignment(
        self,
        fix: Dict[str, Any],
        root_cause: Dict[str, Any]
    ) -> Dict[str, Any]:

        fix_text = str(
            fix.get(
                "root_cause_addressed",
                ""
            )
        ).lower()

        root_text = str(
            root_cause
        ).lower()

        if not fix_text:

            return {

                "name":
                    "root_cause_alignment",

                "passed":
                    False,

                "severity":
                    "warning",

                "message":
                    "Fix does not explicitly describe which root cause it addresses."

            }

        # Basic evidence of overlap.
        root_words = {
            word
            for word in root_text.split()
            if len(word) > 5
        }

        overlap = sum(
            1
            for word in root_words
            if word in fix_text
        )

        passed = overlap >= 1

        return {

            "name":
                "root_cause_alignment",

            "passed":
                passed,

            "severity":
                "info"
                if passed
                else "warning",

            "message":
                "Fix appears aligned with the detected root cause."
                if passed
                else
                "Fix may not directly address the detected root cause."

        }

    # =====================================================
    # FILE VALIDATION
    # =====================================================

    def _check_files(
        self,
        fix: Dict[str, Any],
        project_map: Dict[str, Any]
    ) -> Dict[str, Any]:

        proposed_files = fix.get(
            "affected_files",
            []
        )

        actual_files = project_map.get(
            "files",
            []
        )

        actual_paths = set()

        if isinstance(
            actual_files,
            list
        ):

            for item in actual_files:

                if isinstance(
                    item,
                    str
                ):

                    actual_paths.add(
                        item
                    )

                elif isinstance(
                    item,
                    dict
                ):

                    path = (
                        item.get("path")
                        or item.get("file")
                        or item.get("name")
                    )

                    if path:

                        actual_paths.add(
                            str(path)
                        )

        unknown = []

        if isinstance(
            proposed_files,
            list
        ):

            for file_name in proposed_files:

                if not actual_paths:

                    continue

                if not any(
                    str(file_name) in path
                    or path in str(file_name)
                    for path in actual_paths
                ):

                    unknown.append(
                        str(file_name)
                    )

        if unknown:

            return {

                "name":
                    "file_validation",

                "passed":
                    False,

                "severity":
                    "warning",

                "message":
                    "Fix references files that were not found in the project map: "
                    + ", ".join(unknown)

            }

        return {

            "name":
                "file_validation",

            "passed":
                True,

            "severity":
                "info",

            "message":
                "Affected files are consistent with the available project map."

        }

    # =====================================================
    # FUNCTION VALIDATION
    # =====================================================

    def _check_functions(
        self,
        fix: Dict[str, Any],
        project_map: Dict[str, Any]
    ) -> Dict[str, Any]:

        proposed_functions = fix.get(
            "affected_functions",
            []
        )

        actual_functions = project_map.get(
            "functions",
            []
        )

        actual_names = set()

        if isinstance(
            actual_functions,
            list
        ):

            for item in actual_functions:

                if isinstance(
                    item,
                    str
                ):

                    actual_names.add(
                        item
                    )

                elif isinstance(
                    item,
                    dict
                ):

                    name = item.get(
                        "name"
                    )

                    if name:

                        actual_names.add(
                            str(name)
                        )

        unknown = []

        if isinstance(
            proposed_functions,
            list
        ):

            for function in proposed_functions:

                if (
                    actual_names
                    and str(function)
                    not in actual_names
                ):

                    unknown.append(
                        str(function)
                    )

        if unknown:

            return {

                "name":
                    "function_validation",

                "passed":
                    False,

                "severity":
                    "warning",

                "message":
                    "Fix references functions that were not found: "
                    + ", ".join(unknown)

            }

        return {

            "name":
                "function_validation",

            "passed":
                True,

            "severity":
                "info",

            "message":
                "Affected functions are consistent with the available project map."

        }

    # =====================================================
    # CODE CHANGE SAFETY
    # =====================================================

    def _check_code_changes(
        self,
        fix: Dict[str, Any]
    ) -> Dict[str, Any]:

        code_changes = fix.get(
            "code_changes",
            []
        )

        if not code_changes:

            return {

                "name":
                    "code_change_safety",

                "passed":
                    True,

                "severity":
                    "info",

                "message":
                    "No direct code change was proposed."

            }

        dangerous_patterns = [

            "disable authentication",

            "disable authorization",

            "remove validation",

            "disable security",

            "ignore ssl",

            "turn off security",

            "hardcode password",

            "hardcode secret",

            "expose api key",

            "remove logging"

        ]

        suspicious = []

        for change in code_changes:

            text = str(
                change
            ).lower()

            for pattern in dangerous_patterns:

                if pattern in text:

                    suspicious.append(
                        pattern
                    )

        if suspicious:

            return {

                "name":
                    "code_change_safety",

                "passed":
                    False,

                "severity":
                    "error",

                "message":
                    "Potentially unsafe remediation detected: "
                    + ", ".join(
                        sorted(
                            set(suspicious)
                        )
                    )

            }

        return {

            "name":
                "code_change_safety",

            "passed":
                True,

            "severity":
                "info",

            "message":
                "No obvious unsafe remediation pattern was detected."

        }

    # =====================================================
    # ROLLBACK PLAN
    # =====================================================

    def _check_rollback(
        self,
        fix: Dict[str, Any]
    ) -> Dict[str, Any]:

        rollback = fix.get(
            "rollback_plan",
            []
        )

        if rollback:

            return {

                "name":
                    "rollback_plan",

                "passed":
                    True,

                "severity":
                    "info",

                "message":
                    "Rollback instructions are provided."

            }

        return {

            "name":
                "rollback_plan",

            "passed":
                False,

            "severity":
                "warning",

            "message":
                "No rollback plan was provided."

        }

    # =====================================================
    # VERIFICATION
    # =====================================================

    def _check_verification(
        self,
        fix: Dict[str, Any]
    ) -> Dict[str, Any]:

        verification = fix.get(
            "verification",
            []
        )

        if verification:

            return {

                "name":
                    "verification",

                "passed":
                    True,

                "severity":
                    "info",

                "message":
                    "Verification steps are provided."

            }

        return {

            "name":
                "verification",

            "passed":
                False,

            "severity":
                "warning",

            "message":
                "No verification steps were provided."

        }

    # =====================================================
    # SECURITY
    # =====================================================

    def _check_security(
        self,
        fix: Dict[str, Any]
    ) -> Dict[str, Any]:

        text = str(
            fix
        ).lower()

        dangerous = [

            "password",
            "api key",
            "secret",
            "token",
            "private key"

        ]

        suspicious = []

        for keyword in dangerous:

            if keyword in text:

                suspicious.append(
                    keyword
                )

        # Presence of a secret-related word alone
        # isn't an error. We only flag it as a warning
        # so a human can review it.

        if suspicious:

            return {

                "name":
                    "security_review",

                "passed":
                    True,

                "severity":
                    "warning",

                "message":
                    "Fix references security-sensitive configuration. "
                    "Review it before deployment."

            }

        return {

            "name":
                "security_review",

            "passed":
                True,

            "severity":
                "info",

            "message":
                "No security-sensitive remediation was detected."

        }

    # =====================================================
    # SCORE
    # =====================================================

    def _calculate_score(
        self,
        checks: List[Dict[str, Any]]
    ) -> float:

        if not checks:
            return 0

        score = 0

        for check in checks:

            if check["passed"]:

                score += 1

            elif check["severity"] == "warning":

                score += 0.5

        return round(
            (
                score
                / len(checks)
            ) * 100,
            2
        )

    # =====================================================
    # STATUS
    # =====================================================

    def _get_status(
        self,
        score: float,
        checks: List[Dict[str, Any]]
    ) -> str:

        has_error = any(
            check["severity"] == "error"
            and not check["passed"]
            for check in checks
        )

        if has_error:
            return "rejected"

        if score >= 85:
            return "approved"

        if score >= 65:
            return "needs_review"

        return "rejected"

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    def _recommendation(
        self,
        status: str
    ) -> str:

        if status == "approved":

            return (
                "Fix passed validation and can be "
                "considered for implementation after "
                "normal engineering review."
            )

        if status == "needs_review":

            return (
                "Fix contains warnings and should be "
                "reviewed by an engineer before implementation."
            )

        return (
            "Fix should not be applied automatically. "
            "Review the validation errors and regenerate "
            "the remediation."
        )


# =========================================================
# SIMPLE HELPER
# =========================================================

def validate_fix(
    fix,
    root_cause=None,
    impact=None,
    project_map=None
):

    validator = FixValidator()

    return validator.validate(

        fix=fix,

        root_cause=root_cause,

        impact=impact,

        project_map=project_map

    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    import json

    fix = {

        "title":
            "Handle database connection exhaustion",

        "summary":
            "Improve connection handling.",

        "root_cause_addressed":
            "Database connection pool exhaustion",

        "affected_files": [

            "database.py"

        ],

        "affected_functions": [

            "connect_database"

        ],

        "implementation_steps": [

            "Review connection lifecycle.",

            "Ensure connections are released.",

            "Add connection failure handling."

        ],

        "code_changes": [

            {

                "file":
                    "database.py",

                "description":
                    "Release database resources correctly."

            }

        ],

        "rollback_plan": [

            "Revert the database connection changes."

        ],

        "verification": [

            "Run database failure tests.",

            "Run connection recovery tests."

        ],

        "confidence":
            0.92

    }

    root_cause = {

        "root_cause":
            "Database connection pool exhaustion",

        "confidence":
            0.94

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

    validator = FixValidator()

    result = validator.validate(

        fix=fix,

        root_cause=root_cause,

        project_map=project_map

    )

    print()

    print("=" * 70)

    print(
        "             CHAOSPILOT FIX VALIDATOR"
    )

    print("=" * 70)

    print()

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    print()

    print("=" * 70)