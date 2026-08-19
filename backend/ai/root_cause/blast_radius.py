from typing import Any, Dict, List, Optional, Set


# =========================================================
# CHAOSPILOT BLAST RADIUS ANALYZER
# =========================================================


class BlastRadiusAnalyzer:

    def __init__(self):
        pass

    # =====================================================
    # ANALYZE BLAST RADIUS
    # =====================================================

    def analyze(
        self,
        failure_location: Optional[Dict[str, Any]] = None,
        project_map: Optional[Dict[str, Any]] = None,
        call_graph: Optional[Any] = None,
        dependencies: Optional[Any] = None
    ) -> Dict[str, Any]:

        failure_location = failure_location or {}
        project_map = project_map or {}

        failure_file = failure_location.get("file")
        failure_function = failure_location.get("function")

        affected_files: Set[str] = set()
        affected_functions: Set[str] = set()
        affected_dependencies: Set[str] = set()

        # -------------------------------------------------
        # FAILURE FILE
        # -------------------------------------------------

        if failure_file:
            affected_files.add(
                str(failure_file)
            )

        # -------------------------------------------------
        # FAILURE FUNCTION
        # -------------------------------------------------

        if failure_function:
            affected_functions.add(
                str(failure_function)
            )

        # -------------------------------------------------
        # CALL GRAPH ANALYSIS
        # -------------------------------------------------

        graph = call_graph

        if graph is None:
            graph = project_map.get(
                "call_graph",
                []
            )

        self._trace_call_graph(
            graph=graph,
            failure_function=failure_function,
            affected_functions=affected_functions,
            affected_files=affected_files
        )

        # -------------------------------------------------
        # DEPENDENCY ANALYSIS
        # -------------------------------------------------

        dependency_data = dependencies

        if dependency_data is None:
            dependency_data = project_map.get(
                "dependencies",
                []
            )

        self._trace_dependencies(
            dependency_data=dependency_data,
            failure_file=failure_file,
            affected_dependencies=affected_dependencies
        )

        # -------------------------------------------------
        # PROJECT FILE ANALYSIS
        # -------------------------------------------------

        self._trace_project_files(
            project_map=project_map,
            failure_file=failure_file,
            affected_files=affected_files
        )

        # -------------------------------------------------
        # CALCULATE SCORE
        # -------------------------------------------------

        score = self._calculate_score(
            affected_files=affected_files,
            affected_functions=affected_functions,
            affected_dependencies=affected_dependencies
        )

        level = self._get_level(
            score
        )

        # -------------------------------------------------
        # RETURN RESULT
        # -------------------------------------------------

        return {

            "success": True,

            "blast_radius": level,

            "score": score,

            "affected_files":
                sorted(
                    affected_files
                ),

            "affected_functions":
                sorted(
                    affected_functions
                ),

            "affected_dependencies":
                sorted(
                    affected_dependencies
                ),

            "counts": {

                "files":
                    len(affected_files),

                "functions":
                    len(affected_functions),

                "dependencies":
                    len(affected_dependencies)

            },

            "summary":
                self._build_summary(
                    level=level,
                    affected_files=affected_files,
                    affected_functions=affected_functions,
                    affected_dependencies=affected_dependencies
                )

        }

    # =====================================================
    # TRACE CALL GRAPH
    # =====================================================

    def _trace_call_graph(
        self,
        graph: Any,
        failure_function: Optional[str],
        affected_functions: Set[str],
        affected_files: Set[str]
    ):

        if not graph:
            return

        # -------------------------------------------------
        # DICTIONARY CALL GRAPH
        #
        # {
        #   "function_a": ["function_b"],
        #   "function_b": ["function_c"]
        # }
        # -------------------------------------------------

        if isinstance(
            graph,
            dict
        ):

            changed = True

            while changed:

                changed = False

                for caller, calls in graph.items():

                    if not isinstance(
                        calls,
                        list
                    ):
                        continue

                    # Directly calls failure function
                    if failure_function in calls:

                        if caller not in affected_functions:

                            affected_functions.add(
                                caller
                            )

                            changed = True

                    # Calls an already affected function
                    for call in calls:

                        if call in affected_functions:

                            if caller not in affected_functions:

                                affected_functions.add(
                                    caller
                                )

                                changed = True

            return

        # -------------------------------------------------
        # LIST CALL GRAPH
        # -------------------------------------------------

        if isinstance(
            graph,
            list
        ):

            for item in graph:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                caller = (
                    item.get("caller")
                    or item.get("function")
                    or item.get("source")
                )

                calls = (
                    item.get("calls")
                    or item.get("called_functions")
                    or []
                )

                if not isinstance(
                    calls,
                    list
                ):
                    continue

                if (
                    failure_function
                    and failure_function in calls
                ):

                    if caller:
                        affected_functions.add(
                            str(caller)
                        )

    # =====================================================
    # TRACE DEPENDENCIES
    # =====================================================

    def _trace_dependencies(
        self,
        dependency_data: Any,
        failure_file: Optional[str],
        affected_dependencies: Set[str]
    ):

        if not dependency_data:
            return

        if isinstance(
            dependency_data,
            list
        ):

            for item in dependency_data:

                if isinstance(
                    item,
                    str
                ):

                    affected_dependencies.add(
                        item
                    )

                elif isinstance(
                    item,
                    dict
                ):

                    name = (
                        item.get("name")
                        or item.get("module")
                        or item.get("dependency")
                    )

                    if name:

                        affected_dependencies.add(
                            str(name)
                        )

        elif isinstance(
            dependency_data,
            dict
        ):

            for key, value in dependency_data.items():

                affected_dependencies.add(
                    str(key)
                )

                if isinstance(
                    value,
                    list
                ):

                    for dependency in value:

                        affected_dependencies.add(
                            str(dependency)
                        )

    # =====================================================
    # TRACE PROJECT FILES
    # =====================================================

    def _trace_project_files(
        self,
        project_map: Dict[str, Any],
        failure_file: Optional[str],
        affected_files: Set[str]
    ):

        if not failure_file:
            return

        files = project_map.get(
            "files",
            []
        )

        if not isinstance(
            files,
            list
        ):
            return

        for item in files:

            if isinstance(
                item,
                str
            ):

                if failure_file in item:

                    affected_files.add(
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

                if path and failure_file in str(path):

                    affected_files.add(
                        str(path)
                    )

    # =====================================================
    # CALCULATE SCORE
    # =====================================================

    def _calculate_score(
        self,
        affected_files: Set[str],
        affected_functions: Set[str],
        affected_dependencies: Set[str]
    ) -> int:

        return (

            len(affected_files) * 3

            + len(affected_functions) * 2

            + len(affected_dependencies)

        )

    # =====================================================
    # GET BLAST RADIUS LEVEL
    # =====================================================

    def _get_level(
        self,
        score: int
    ) -> str:

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
    # BUILD SUMMARY
    # =====================================================

    def _build_summary(
        self,
        level: str,
        affected_files: Set[str],
        affected_functions: Set[str],
        affected_dependencies: Set[str]
    ) -> str:

        return (
            f"The estimated blast radius is {level}. "
            f"{len(affected_files)} file(s), "
            f"{len(affected_functions)} function(s), "
            f"and {len(affected_dependencies)} "
            f"dependency/dependencies may be affected."
        )


# =========================================================
# SIMPLE HELPER
# =========================================================

def analyze_blast_radius(
    failure_location,
    project_map=None,
    call_graph=None,
    dependencies=None
):

    analyzer = BlastRadiusAnalyzer()

    return analyzer.analyze(

        failure_location=failure_location,

        project_map=project_map,

        call_graph=call_graph,

        dependencies=dependencies

    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("          CHAOSPILOT BLAST RADIUS ANALYZER")
    print("=" * 70)

    failure_location = {

        "file":
            "database.py",

        "function":
            "connect_database",

        "line":
            42

    }

    project_map = {

        "files": [

            "app.py",

            "database.py",

            "payment.py",

            "orders.py"

        ],

        "call_graph": {

            "process_payment": [
                "connect_database"
            ],

            "create_order": [
                "process_payment"
            ]

        },

        "dependencies": [

            "sqlite3",

            "payment_service",

            "order_service"

        ]

    }

    result = analyze_blast_radius(

        failure_location=failure_location,

        project_map=project_map

    )

    print()

    print(
        result
    )

    print()
    print("=" * 70)