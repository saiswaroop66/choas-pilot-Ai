from datetime import datetime
from uuid import uuid4


# =========================================================
# CHAOSPILOT REPORT GENERATOR
# =========================================================

class ReportGenerator:

    def generate(
        self,
        application_id,
        project_map=None,
        failure_evidence=None,
        chaos_result=None,
        root_cause=None
    ):

        failure_evidence = failure_evidence or {}
        chaos_result = chaos_result or {}

        failure_location = (
            failure_evidence.get(
                "failure_location"
            )
            or {}
        )

        exception = (
            failure_evidence.get(
                "exception"
            )
            or {}
        )

        report = {

            "report_id": str(
                uuid4()
            ),

            "application_id":
                application_id,

            "generated_at":
                datetime.utcnow().isoformat(),

            "summary":
                self._build_summary(
                    exception,
                    failure_location
                ),

            "failure": {

                "type":
                    exception.get("type"),

                "message":
                    exception.get("message"),

                "file":
                    failure_location.get("file"),

                "function":
                    failure_location.get("function"),

                "line":
                    failure_location.get("line")

            },

            "root_cause":
                root_cause,

            "project": self._project_summary(
                project_map
            ),

            "chaos": self._chaos_summary(
                chaos_result
            ),

            "recommendations": [],

            "status":
                "generated"

        }

        return report


    # =====================================================
    # SUMMARY
    # =====================================================

    def _build_summary(
        self,
        exception,
        location
    ):

        error_type = (
            exception.get("type")
            or "Unknown error"
        )

        file_name = (
            location.get("file")
            or "Unknown file"
        )

        function = (
            location.get("function")
            or "Unknown function"
        )

        line = (
            location.get("line")
            or "Unknown"
        )

        return (
            f"{error_type} detected in "
            f"{file_name}, function "
            f"{function}, line {line}."
        )


    # =====================================================
    # PROJECT SUMMARY
    # =====================================================

    def _project_summary(
        self,
        project_map
    ):

        if not project_map:

            return {
                "available": False
            }

        project = project_map.get(
            "project",
            {}
        )

        total_functions = 0
        total_dependencies = 0
        total_calls = 0


        for file_info in project_map.get(
            "functions",
            []
        ):

            if "error" not in file_info:

                total_functions += len(
                    file_info.get(
                        "functions",
                        []
                    )
                )


        for file_info in project_map.get(
            "dependencies",
            []
        ):

            if "error" not in file_info:

                total_dependencies += len(
                    file_info.get(
                        "dependencies",
                        []
                    )
                )


        for file_info in project_map.get(
            "call_graph",
            []
        ):

            if "error" in file_info:
                continue

            for function in file_info.get(
                "functions",
                []
            ):

                total_calls += len(
                    function.get(
                        "calls",
                        []
                    )
                )


        return {

            "available": True,

            "total_files":
                project.get(
                    "total_files",
                    0
                ),

            "supported_files":
                project.get(
                    "supported_files",
                    0
                ),

            "total_functions":
                total_functions,

            "total_dependencies":
                total_dependencies,

            "total_function_calls":
                total_calls

        }


    # =====================================================
    # CHAOS SUMMARY
    # =====================================================

    def _chaos_summary(
        self,
        chaos_result
    ):

        if not chaos_result:

            return {
                "available": False
            }


        experiment = chaos_result.get(
            "experiment",
            {}
        )

        result = experiment.get(
            "result",
            {}
        )


        return {

            "available": True,

            "experiment":
                experiment.get(
                    "name"
                ),

            "type":
                experiment.get(
                    "experiment_type"
                ),

            "status":
                experiment.get(
                    "status"
                ),

            "recovered":
                result.get(
                    "recovered"
                ),

            "impact":
                result.get(
                    "impact"
                )

        }


# =========================================================
# SIMPLE FUNCTION
# =========================================================

def generate_report(
    application_id,
    project_map=None,
    failure_evidence=None,
    chaos_result=None,
    root_cause=None
):

    generator = ReportGenerator()

    return generator.generate(

        application_id=application_id,

        project_map=project_map,

        failure_evidence=failure_evidence,

        chaos_result=chaos_result,

        root_cause=root_cause

    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    report = generate_report(

        application_id=1,

        failure_evidence={

            "exception": {

                "type":
                    "ConnectionError",

                "message":
                    "Database unavailable"

            },

            "failure_location": {

                "file":
                    "database.py",

                "function":
                    "connect_database",

                "line":
                    42

            }

        },

        root_cause=(
            "Database connection pool "
            "was exhausted."
        )

    )

    print()
    print("=" * 70)
    print("             CHAOSPILOT REPORT GENERATOR")
    print("=" * 70)

    print()

    print(
        report
    )

    print()
    print("=" * 70)