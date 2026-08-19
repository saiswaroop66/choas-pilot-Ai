from typing import Any, Dict, List, Optional
import re


# =========================================================
# CHAOSPILOT FAILURE DETECTOR
# =========================================================


class FailureDetector:

    def __init__(self):
        self.failure_patterns = self._load_patterns()

    # =====================================================
    # FAILURE PATTERNS
    # =====================================================

    def _load_patterns(self):

        return {

            "database": [
                "database",
                "sql",
                "sqlite",
                "postgres",
                "mysql",
                "mongodb",
                "connection pool",
                "connection refused",
                "database connection"
            ],

            "network": [
                "network",
                "timeout",
                "connection refused",
                "connection reset",
                "dns",
                "socket",
                "unreachable",
                "http error"
            ],

            "authentication": [
                "authentication",
                "unauthorized",
                "forbidden",
                "invalid token",
                "jwt",
                "permission denied",
                "access denied"
            ],

            "memory": [
                "out of memory",
                "memory error",
                "memoryerror",
                "heap",
                "allocation failed"
            ],

            "cpu": [
                "cpu",
                "high cpu",
                "cpu limit",
                "resource exhausted"
            ],

            "dependency": [
                "module not found",
                "import error",
                "dependency",
                "package",
                "library not found",
                "no module named"
            ],

            "file_system": [
                "file not found",
                "filenotfounderror",
                "permission denied",
                "directory",
                "filesystem",
                "disk full"
            ],

            "configuration": [
                "configuration",
                "config",
                "environment variable",
                "missing environment",
                "invalid configuration"
            ],

            "validation": [
                "validation error",
                "invalid input",
                "invalid value",
                "schema",
                "required field"
            ],

            "runtime": [
                "runtimeerror",
                "exception",
                "unexpected error",
                "runtime error"
            ]
        }

    # =====================================================
    # DETECT FAILURE
    # =====================================================

    def detect(
        self,
        failure: Optional[Any] = None,
        logs: Optional[Any] = None,
        stack_trace: Optional[str] = None
    ) -> Dict[str, Any]:

        text = self._combine_evidence(
            failure=failure,
            logs=logs,
            stack_trace=stack_trace
        )

        normalized_text = text.lower()

        categories = self._detect_categories(
            normalized_text
        )

        exception_type = self._extract_exception(
            text
        )

        location = self._extract_location(
            stack_trace
        )

        severity = self._estimate_severity(
            normalized_text,
            categories
        )

        signals = self._extract_signals(
            normalized_text
        )

        return {

            "success": True,

            "detected": bool(
                categories
                or exception_type
                or location
            ),

            "failure_type":
                self._primary_category(
                    categories
                ),

            "categories":
                categories,

            "exception_type":
                exception_type,

            "severity":
                severity,

            "failure_location":
                location,

            "signals":
                signals,

            "summary":
                self._build_summary(
                    categories=categories,
                    exception_type=exception_type,
                    location=location,
                    severity=severity
                )

        }

    # =====================================================
    # COMBINE EVIDENCE
    # =====================================================

    def _combine_evidence(
        self,
        failure,
        logs,
        stack_trace
    ) -> str:

        parts = []

        if failure:

            parts.append(
                str(failure)
            )

        if logs:

            if isinstance(
                logs,
                list
            ):

                parts.extend(
                    str(item)
                    for item in logs
                )

            else:

                parts.append(
                    str(logs)
                )

        if stack_trace:

            parts.append(
                stack_trace
            )

        return "\n".join(
            parts
        )

    # =====================================================
    # DETECT CATEGORIES
    # =====================================================

    def _detect_categories(
        self,
        text: str
    ) -> List[Dict[str, Any]]:

        matches = []

        for category, patterns in (
            self.failure_patterns.items()
        ):

            category_matches = []

            for pattern in patterns:

                if pattern.lower() in text:

                    category_matches.append(
                        pattern
                    )

            if category_matches:

                matches.append({

                    "category":
                        category,

                    "matched_patterns":
                        category_matches,

                    "score":
                        len(
                            category_matches
                        )

                })

        matches.sort(
            key=lambda item:
                item["score"],
            reverse=True
        )

        return matches

    # =====================================================
    # EXTRACT EXCEPTION
    # =====================================================

    def _extract_exception(
        self,
        text: str
    ) -> Optional[str]:

        common_exceptions = [

            "ConnectionError",

            "ConnectionRefusedError",

            "TimeoutError",

            "FileNotFoundError",

            "PermissionError",

            "MemoryError",

            "ImportError",

            "ModuleNotFoundError",

            "ValueError",

            "TypeError",

            "KeyError",

            "IndexError",

            "RuntimeError",

            "OSError",

            "DatabaseError",

            "OperationalError",

            "AuthenticationError"

        ]

        for exception in common_exceptions:

            if exception.lower() in text.lower():

                return exception

        # Generic Python exception pattern
        match = re.search(

            r"\b([A-Za-z_][A-Za-z0-9_]*Error)\b",

            text

        )

        if match:

            return match.group(1)

        return None

    # =====================================================
    # EXTRACT FILE / FUNCTION / LINE
    # =====================================================

    def _extract_location(
        self,
        stack_trace: Optional[str]
    ) -> Dict[str, Any]:

        if not stack_trace:

            return {

                "file": None,

                "function": None,

                "line": None

            }

        file_name = None
        line_number = None
        function_name = None

        # Python traceback:
        # File "database.py", line 42
        match = re.search(

            r'File\s+["\']([^"\']+)["\']'
            r',\s*line\s+(\d+)',

            stack_trace

        )

        if match:

            file_name = match.group(1)

            line_number = int(
                match.group(2)
            )

        # Python traceback:
        # in connect_database
        function_match = re.search(

            r'\bin\s+([A-Za-z_][A-Za-z0-9_]*)',

            stack_trace

        )

        if function_match:

            function_name = (
                function_match.group(1)
            )

        return {

            "file":
                file_name,

            "function":
                function_name,

            "line":
                line_number

        }

    # =====================================================
    # ESTIMATE SEVERITY
    # =====================================================

    def _estimate_severity(
        self,
        text: str,
        categories: List[Dict[str, Any]]
    ) -> str:

        critical_keywords = [

            "critical",

            "fatal",

            "system down",

            "service unavailable",

            "out of memory",

            "data loss",

            "production down",

            "database unavailable"

        ]

        high_keywords = [

            "error",

            "exception",

            "connection refused",

            "timeout",

            "failed",

            "unavailable"

        ]

        if any(
            keyword in text
            for keyword in critical_keywords
        ):

            return "critical"

        if any(
            keyword in text
            for keyword in high_keywords
        ):

            return "high"

        if categories:

            return "medium"

        return "low"

    # =====================================================
    # EXTRACT SIGNALS
    # =====================================================

    def _extract_signals(
        self,
        text: str
    ) -> List[str]:

        signals = []

        signal_patterns = {

            "timeout":
                r"\btimeout\b",

            "connection_refused":
                r"connection refused",

            "permission_denied":
                r"permission denied",

            "not_found":
                r"not found",

            "out_of_memory":
                r"out of memory",

            "authentication_failure":
                r"authentication|unauthorized",

            "dependency_failure":
                r"module not found|no module named"

        }

        for name, pattern in (
            signal_patterns.items()
        ):

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                signals.append(
                    name
                )

        return signals

    # =====================================================
    # PRIMARY CATEGORY
    # =====================================================

    def _primary_category(
        self,
        categories: List[Dict[str, Any]]
    ) -> Optional[str]:

        if not categories:

            return None

        return categories[0].get(
            "category"
        )

    # =====================================================
    # BUILD SUMMARY
    # =====================================================

    def _build_summary(
        self,
        categories,
        exception_type,
        location,
        severity
    ) -> str:

        failure_type = (
            categories[0]["category"]
            if categories
            else "unknown"
        )

        location_text = ""

        if location.get("file"):

            location_text = (
                f" at {location['file']}"
            )

            if location.get("line"):

                location_text += (
                    f":{location['line']}"
                )

        exception_text = ""

        if exception_type:

            exception_text = (
                f" ({exception_type})"
            )

        return (
            f"{severity.capitalize()} "
            f"{failure_type} failure"
            f"{exception_text}"
            f"{location_text}."
        )


# =========================================================
# SIMPLE HELPER
# =========================================================

def detect_failure(
    failure=None,
    logs=None,
    stack_trace=None
):

    detector = FailureDetector()

    return detector.detect(

        failure=failure,

        logs=logs,

        stack_trace=stack_trace

    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("             CHAOSPILOT FAILURE DETECTOR")
    print("=" * 70)

    failure = {

        "type":
            "ConnectionError",

        "message":
            "Database connection failed",

        "severity":
            "critical"

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

    detector = FailureDetector()

    result = detector.detect(

        failure=failure,

        logs=logs,

        stack_trace=stack_trace

    )

    print()

    print(result)

    print()
    print("=" * 70)