from typing import Any, Dict, List, Optional, Set


# =========================================================
# CHAOSPILOT IMPACT ANALYZER
# =========================================================


class ImpactAnalyzer:

    def __init__(self):
        pass

    # =====================================================
    # ANALYZE IMPACT
    # =====================================================

    def analyze(
        self,
        root_cause: Optional[Dict[str, Any]] = None,
        project_map: Optional[Dict[str, Any]] = None,
        failure: Optional[Dict[str, Any]] = None,
        chaos_result: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        root_cause = root_cause or {}
        project_map = project_map or {}
        failure = failure or {}
        chaos_result = chaos_result or {}

        # -------------------------------------------------
        # FAILURE LOCATION
        # -------------------------------------------------

        location = self._extract_location(
            root_cause
        )

        failure_file = location.get("file")
        failure_function = location.get("function")

        # -------------------------------------------------
        # FIND AFFECTED COMPONENTS
        # -------------------------------------------------

        affected_files = self._find_affected_files(
            failure_file,
            project_map
        )

        affected_functions = self._find_affected_functions(
            failure_function,
            project_map
        )

        affected_dependencies = self._find_dependencies(
            project_map
        )

        affected_services = self._find_services(
            project_map,
            failure_file,
            failure_function
        )

        # -------------------------------------------------
        # CHAOS IMPACT
        # -------------------------------------------------

        chaos_impact = self._analyze_chaos(
            chaos_result
        )

        # -------------------------------------------------
        # SEVERITY
        # -------------------------------------------------

        severity = self._calculate_severity(
            failure=failure,
            chaos_impact=chaos_impact,
            affected_files=affected_files,
            affected_functions=affected_functions,
            affected_services=affected_services
        )

        # -------------------------------------------------
        # BUSINESS IMPACT
        # -------------------------------------------------

        business_impact = self._estimate_business_impact(
            severity=severity,
            failure=failure,
            affected_services=affected_services
        )

        # -------------------------------------------------
        # BLAST RADIUS
        # -------------------------------------------------

        blast_radius = self._calculate_blast_radius(
            affected_files=affected_files,
            affected_functions=affected_functions,
            affected_dependencies=affected_dependencies,
            affected_services=affected_services
        )

        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        recommendations = self._recommendations(
            severity=severity,
            blast_radius=blast_radius
        )

        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------

        return {

            "success": True,

            "severity": severity,

            "blast_radius": blast_radius,

            "failure_location": {

                "file": failure_file,

                "function": failure_function,

                "line": location.get("line")

            },

            "affected": {

                "files": affected_files,

                "functions": affected_functions,

                "dependencies": affected_dependencies,

                "services": affected_services

            },

            "chaos_impact": chaos_impact,

            "business_impact": business_impact,

            "recommendations": recommendations,

            "summary": self._build_summary(
                severity=severity,
                blast_radius=blast_radius,
                affected_files=affected_files,
                affected_functions=affected_functions,
                affected_services=affected_services
            )

        }

    # =====================================================
    # EXTRACT FAILURE LOCATION
    # =====================================================

    def _extract_location(
        self,
        root_cause: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not root_cause:
            return {}

        # Direct location
        location = root_cause.get(
            "failure_location"
        )

        if isinstance(location, dict):
            return location

        # Nested analysis
        analysis = root_cause.get(
            "analysis"
        )

        if isinstance(analysis, dict):

            location = analysis.get(
                "failure_location"
            )

            if isinstance(location, dict):
                return location

        # Nested root cause
        nested = root_cause.get(
            "root_cause"
        )

        if isinstance(nested, dict):

            location = nested.get(
                "failure_location"
            )

            if isinstance(location, dict):
                return location

        return {}

    # =====================================================
    # FIND AFFECTED FILES
    # =====================================================

    def _find_affected_files(
        self,
        failure_file: Optional[str],
        project_map: Dict[str, Any]
    ) -> List[str]:

        if not failure_file:
            return []

        affected: Set[str] = set()

        files = project_map.get(
            "files",
            []
        )

        if not isinstance(files, list):
            return []

        for item in files:

            if isinstance(item, str):

                if failure_file in item:
                    affected.add(item)

            elif isinstance(item, dict):

                path = (
                    item.get("path")
                    or item.get("file")
                    or item.get("name")
                )

                if path and failure_file in str(path):
                    affected.add(str(path))

        return sorted(affected)

    # =====================================================
    # FIND AFFECTED FUNCTIONS
    # =====================================================

    def _find_affected_functions(
        self,
        failure_function: Optional[str],
        project_map: Dict[str, Any]
    ) -> List[str]:

        if not failure_function:
            return []

        affected: Set[str] = {
            failure_function
        }

        functions = project_map.get(
            "functions",
            []
        )

        if not isinstance(functions, list):
            return sorted(affected)

        for item in functions:

            if not isinstance(item, dict):
                continue

            name = item.get("name")

            calls = item.get(
                "calls",
                []
            )

            if (
                isinstance(calls, list)
                and failure_function in calls
                and name
            ):

                affected.add(name)

        return sorted(affected)

    # =====================================================
    # FIND DEPENDENCIES
    # =====================================================

    def _find_dependencies(
        self,
        project_map: Dict[str, Any]
    ) -> List[str]:

        dependencies: Set[str] = set()

        data = project_map.get(
            "dependencies",
            []
        )

        if isinstance(data, list):

            for item in data:

                if isinstance(item, str):
                    dependencies.add(item)

                elif isinstance(item, dict):

                    name = (
                        item.get("name")
                        or item.get("module")
                        or item.get("dependency")
                    )

                    if name:
                        dependencies.add(str(name))

        return sorted(dependencies)

    # =====================================================
    # FIND SERVICES
    # =====================================================

    def _find_services(
        self,
        project_map: Dict[str, Any],
        failure_file: Optional[str],
        failure_function: Optional[str]
    ) -> List[str]:

        services: Set[str] = set()

        service_data = project_map.get(
            "services",
            []
        )

        if isinstance(service_data, list):

            for service in service_data:

                if isinstance(service, str):

                    services.add(service)

                elif isinstance(service, dict):

                    name = (
                        service.get("name")
                        or service.get("service")
                    )

                    files = service.get(
                        "files",
                        []
                    )

                    functions = service.get(
                        "functions",
                        []
                    )

                    matches = (
                        failure_file in files
                        if failure_file
                        and isinstance(files, list)
                        else False
                    )

                    function_matches = (
                        failure_function in functions
                        if failure_function
                        and isinstance(functions, list)
                        else False
                    )

                    if (
                        name
                        and (
                            matches
                            or function_matches
                        )
                    ):

                        services.add(str(name))

        return sorted(services)

    # =====================================================
    # ANALYZE CHAOS RESULT
    # =====================================================

    def _analyze_chaos(
        self,
        chaos_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not chaos_result:

            return {
                "available": False,
                "error_rate": 0,
                "request_delay": 0,
                "service_available": None,
                "recovered": None
            }

        impact = chaos_result.get(
            "impact",
            {}
        )

        if not isinstance(impact, dict):
            impact = {}

        return {

            "available": True,

            "error_rate":
                impact.get(
                    "error_rate",
                    0
                ),

            "request_delay":
                impact.get(
                    "request_delay",
                    0
                ),

            "service_available":
                impact.get(
                    "service_available"
                ),

            "recovered":
                chaos_result.get(
                    "recovered"
                )

        }

    # =====================================================
    # CALCULATE SEVERITY
    # =====================================================

    def _calculate_severity(
        self,
        failure: Dict[str, Any],
        chaos_impact: Dict[str, Any],
        affected_files: List[str],
        affected_functions: List[str],
        affected_services: List[str]
    ) -> str:

        declared = str(
            failure.get(
                "severity",
                ""
            )
        ).lower()

        if declared in {
            "critical",
            "high"
        }:
            return declared

        try:
            error_rate = float(
                chaos_impact.get(
                    "error_rate",
                    0
                )
            )
        except (
            TypeError,
            ValueError
        ):
            error_rate = 0

        if error_rate >= 80:
            return "critical"

        if error_rate >= 40:
            return "high"

        if len(affected_services) >= 3:
            return "high"

        if (
            len(affected_files) >= 3
            or len(affected_functions) >= 5
        ):
            return "medium"

        return "low"

    # =====================================================
    # BLAST RADIUS
    # =====================================================

    def _calculate_blast_radius(
        self,
        affected_files: List[str],
        affected_functions: List[str],
        affected_dependencies: List[str],
        affected_services: List[str]
    ) -> str:

        score = (

            len(affected_files) * 2

            + len(affected_functions)

            + len(affected_dependencies)

            + len(affected_services) * 4

        )

        if score >= 20:
            return "very_high"

        if score >= 12:
            return "high"

        if score >= 6:
            return "medium"

        if score >= 3:
            return "low"

        return "minimal"

    # =====================================================
    # BUSINESS IMPACT
    # =====================================================

    def _estimate_business_impact(
        self,
        severity: str,
        failure: Dict[str, Any],
        affected_services: List[str]
    ) -> Dict[str, Any]:

        if severity == "critical":

            return {
                "level": "critical",
                "description": (
                    "The failure may significantly affect "
                    "application availability or critical "
                    "user operations."
                ),
                "user_impact": "high"
            }

        if severity == "high":

            return {
                "level": "high",
                "description": (
                    "Users may experience failed requests "
                    "or degraded application functionality."
                ),
                "user_impact": "high"
            }

        if severity == "medium":

            return {
                "level": "medium",
                "description": (
                    "Some application functionality may "
                    "be degraded."
                ),
                "user_impact": "moderate"
            }

        return {
            "level": "low",
            "description": (
                "The failure appears localized with "
                "limited user impact."
            ),
            "user_impact": "low"
        }

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def _recommendations(
        self,
        severity: str,
        blast_radius: str
    ) -> List[str]:

        recommendations = []

        if severity in {
            "critical",
            "high"
        }:

            recommendations.append(
                "Prioritize remediation of the affected "
                "component."
            )

            recommendations.append(
                "Add monitoring and alerting around the "
                "failure path."
            )

        if blast_radius in {
            "high",
            "very_high"
        }:

            recommendations.append(
                "Review downstream dependencies for "
                "secondary failures."
            )

            recommendations.append(
                "Add integration tests for the affected "
                "workflow."
            )

        if not recommendations:

            recommendations.append(
                "Continue monitoring the affected "
                "component."
            )

        return recommendations

    # =====================================================
    # SUMMARY
    # =====================================================

    def _build_summary(
        self,
        severity: str,
        blast_radius: str,
        affected_files: List[str],
        affected_functions: List[str],
        affected_services: List[str]
    ) -> str:

        return (
            f"Impact severity is {severity} with a "
            f"{blast_radius} blast radius. "
            f"{len(affected_files)} file(s), "
            f"{len(affected_functions)} function(s), "
            f"and {len(affected_services)} service(s) "
            f"may be affected."
        )


# =========================================================
# HELPER
# =========================================================

def analyze_impact(
    root_cause,
    project_map=None,
    failure=None,
    chaos_result=None
):

    analyzer = ImpactAnalyzer()

    return analyzer.analyze(

        root_cause=root_cause,

        project_map=project_map,

        failure=failure,

        chaos_result=chaos_result

    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    import json

    failure = {

        "type": "ConnectionError",

        "message":
            "Database connection failed",

        "severity":
            "critical"

    }

    root_cause = {

        "failure_location": {

            "file":
                "database.py",

            "function":
                "connect_database",

            "line":
                42

        }

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

    chaos_result = {

        "recovered":
            True,

        "impact": {

            "error_rate":
                85,

            "request_delay":
                500,

            "service_available":
                False

        }

    }

    result = analyze_impact(

        root_cause=root_cause,

        project_map=project_map,

        failure=failure,

        chaos_result=chaos_result

    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
