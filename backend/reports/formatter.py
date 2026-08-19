# =========================================================
# CHAOSPILOT REPORT FORMATTER
# =========================================================


class ReportFormatter:

    # =====================================================
    # FORMAT FOR FRONTEND
    # =====================================================

    def format_for_frontend(self, report):

        if not report:
            return {
                "success": False,
                "message": "No report available."
            }

        failure = report.get(
            "failure",
            {}
        )

        project = report.get(
            "project",
            {}
        )

        chaos = report.get(
            "chaos",
            {}
        )

        return {

            "success": True,

            "report_id":
                report.get("report_id"),

            "application_id":
                report.get("application_id"),

            "generated_at":
                report.get("generated_at"),

            "status":
                report.get("status"),

            "summary":
                report.get("summary"),

            "failure": {

                "type":
                    failure.get("type"),

                "message":
                    failure.get("message"),

                "file":
                    failure.get("file"),

                "function":
                    failure.get("function"),

                "line":
                    failure.get("line")

            },

            "root_cause":
                report.get("root_cause"),

            "project": project,

            "chaos": chaos,

            "recommendations":
                report.get(
                    "recommendations",
                    []
                )

        }


    # =====================================================
    # FORMAT AS TEXT
    # =====================================================

    def format_as_text(self, report):

        if not report:
            return "No report available."


        failure = report.get(
            "failure",
            {}
        )

        lines = [

            "CHAOSPILOT FAILURE REPORT",

            "=" * 60,

            "",

            f"Report ID: "
            f"{report.get('report_id')}",

            f"Application ID: "
            f"{report.get('application_id')}",

            "",

            "SUMMARY",

            "-" * 60,

            report.get(
                "summary",
                "No summary available."
            ),

            "",

            "FAILURE",

            "-" * 60,

            f"Type: "
            f"{failure.get('type')}",

            f"Message: "
            f"{failure.get('message')}",

            f"File: "
            f"{failure.get('file')}",

            f"Function: "
            f"{failure.get('function')}",

            f"Line: "
            f"{failure.get('line')}",

            "",

            "ROOT CAUSE",

            "-" * 60,

            str(
                report.get(
                    "root_cause",
                    "Not available."
                )
            ),

            "",

            "PROJECT",

            "-" * 60,

            f"Total Files: "
            f"{report.get('project', {}).get('total_files', 0)}",

            f"Total Functions: "
            f"{report.get('project', {}).get('total_functions', 0)}",

            f"Total Dependencies: "
            f"{report.get('project', {}).get('total_dependencies', 0)}",

            f"Function Calls: "
            f"{report.get('project', {}).get('total_function_calls', 0)}",

            "",

            "CHAOS ANALYSIS",

            "-" * 60,

            f"Experiment: "
            f"{report.get('chaos', {}).get('experiment')}",

            f"Type: "
            f"{report.get('chaos', {}).get('type')}",

            f"Status: "
            f"{report.get('chaos', {}).get('status')}",

            f"Recovered: "
            f"{report.get('chaos', {}).get('recovered')}",

            "",

            "RECOMMENDATIONS",

            "-" * 60

        ]


        recommendations = report.get(
            "recommendations",
            []
        )


        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                lines.append(
                    f"{index}. {recommendation}"
                )

        else:

            lines.append(
                "No recommendations available."
            )


        return "\n".join(
            lines
        )


    # =====================================================
    # FORMAT FOR AI
    # =====================================================

    def format_for_ai(self, report):

        if not report:
            return {}


        return {

            "failure": report.get(
                "failure",
                {}
            ),

            "root_cause": report.get(
                "root_cause"
            ),

            "project": report.get(
                "project",
                {}
            ),

            "chaos": report.get(
                "chaos",
                {}
            ),

            "recommendations":
                report.get(
                    "recommendations",
                    []
                )

        }


# =========================================================
# SIMPLE FUNCTIONS
# =========================================================

def format_report(report):

    formatter = ReportFormatter()

    return formatter.format_for_frontend(
        report
    )


def format_report_text(report):

    formatter = ReportFormatter()

    return formatter.format_as_text(
        report
    )


def format_report_for_ai(report):

    formatter = ReportFormatter()

    return formatter.format_for_ai(
        report
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sample_report = {

        "report_id": "demo-123",

        "application_id": 1,

        "generated_at":
            "2026-08-19T10:00:00",

        "status":
            "generated",

        "summary":
            "ConnectionError detected in database.py.",

        "failure": {

            "type":
                "ConnectionError",

            "message":
                "Database unavailable",

            "file":
                "database.py",

            "function":
                "connect_database",

            "line":
                42

        },

        "root_cause":
            "Database connection pool exhausted.",

        "project": {

            "total_files":
                12,

            "total_functions":
                24,

            "total_dependencies":
                15,

            "total_function_calls":
                40

        },

        "chaos": {

            "experiment":
                "Database Failure",

            "type":
                "database_failure",

            "status":
                "completed",

            "recovered":
                True

        },

        "recommendations": [

            "Increase database pool capacity.",

            "Add connection timeout handling."

        ]

    }


    formatter = ReportFormatter()


    print()

    print(
        formatter.format_as_text(
            sample_report
        )
    )
