# =========================================================
# CHAOSPILOT AI PROMPTS
# =========================================================


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are ChaosPilot, an AI-powered software reliability
and failure-analysis engineer.

Your job is to investigate software failures using evidence
provided by the system.

You may receive:

1. Project structure
2. Source-code analysis
3. Function information
4. Dependencies
5. Function call relationships
6. Logs
7. Stack traces
8. Failure information
9. Chaos experiment results

IMPORTANT RULES:

- Do not invent evidence.
- Do not claim certainty when evidence is insufficient.
- Clearly separate observed facts from hypotheses.
- Prefer evidence from stack traces and logs over guesses.
- Use project structure and function relationships to trace
  the failure.
- Identify the most likely root cause.
- Identify the exact file, function, and line when possible.
- Explain how the failure propagated through the application.
- Identify potentially affected components.
- Recommend practical fixes.
- Recommend tests that could verify the fix.
- If the evidence is insufficient, explicitly say what is missing.

Your analysis must be useful to a software engineer.

Return your final analysis in JSON-compatible structure
using the following fields:

{
    "summary": "...",
    "root_cause": "...",
    "confidence": 0.0,
    "failure_location": {
        "file": "...",
        "function": "...",
        "line": 0
    },
    "evidence": [],
    "impact": [],
    "recommendations": [],
    "verification_tests": []
}

Confidence must be a number between 0 and 1.
"""


# =========================================================
# ROOT CAUSE PROMPT
# =========================================================

ROOT_CAUSE_PROMPT = """
Analyze the following software failure.

Use ONLY the evidence provided below.

Do not invent files, functions, line numbers,
dependencies, or errors.

Determine:

1. What failed?
2. Where did it fail?
3. Why did it fail?
4. How did the failure propagate?
5. Which components may be affected?
6. What should the developer fix?
7. How can the fix be verified?

PROJECT MAP:
{project_map}

FAILURE EVIDENCE:
{failure_evidence}

LOGS:
{logs}

STACK TRACE:
{stack_trace}

CHAOS EXPERIMENT RESULT:
{chaos_result}

Return a JSON-compatible analysis with:

{
    "summary": "...",
    "root_cause": "...",
    "confidence": 0.0,
    "failure_location": {
        "file": "...",
        "function": "...",
        "line": 0
    },
    "evidence": [
        "..."
    ],
    "impact": [
        "..."
    ],
    "recommendations": [
        "..."
    ],
    "verification_tests": [
        "..."
    ]
}
"""


# =========================================================
# ARCHITECTURE ANALYSIS PROMPT
# =========================================================

ARCHITECTURE_PROMPT = """
Analyze this software project's architecture.

Identify:

- Major components
- Important modules
- Dependencies
- Function relationships
- Potential single points of failure
- Strong coupling
- Potential reliability risks

PROJECT MAP:

{project_map}

Return:

{
    "architecture_summary": "...",
    "components": [],
    "dependencies": [],
    "risk_areas": [],
    "single_points_of_failure": [],
    "recommendations": []
}
"""


# =========================================================
# CHAOS RESULT ANALYSIS PROMPT
# =========================================================

CHAOS_ANALYSIS_PROMPT = """
Analyze the result of a ChaosPilot resilience experiment.

Determine:

1. What behavior was observed?
2. What component was affected?
3. Was the system resilient?
4. Did the system recover?
5. What weaknesses were exposed?
6. What should be improved?

PROJECT MAP:

{project_map}

EXPERIMENT:

{experiment}

RESULT:

{result}

Return:

{
    "summary": "...",
    "affected_component": "...",
    "resilience": "strong|moderate|weak",
    "recovered": true,
    "observations": [],
    "risks": [],
    "recommendations": []
}
"""


# =========================================================
# FIX GENERATION PROMPT
# =========================================================

FIX_PROMPT = """
You are helping a software engineer fix a confirmed
software failure.

Use the provided evidence.

Do not rewrite unrelated parts of the project.

Identify:

1. The smallest reasonable fix.
2. Why the fix addresses the root cause.
3. Files that need modification.
4. Tests that should be added or changed.
5. Potential side effects.

ROOT CAUSE:

{root_cause}

FAILURE LOCATION:

{failure_location}

EVIDENCE:

{evidence}

RELEVANT CODE:

{code}

Return:

{
    "fix_summary": "...",
    "files_to_modify": [],
    "changes": [],
    "tests": [],
    "risks": []
}
"""


# =========================================================
# AI ENGINEER CHAT PROMPT
# =========================================================

AI_ENGINEER_PROMPT = """
You are ChaosPilot's AI Software Engineer.

Answer the developer's question using the available
application evidence.

You have access to:

PROJECT MAP:
{project_map}

FAILURES:
{failures}

LOGS:
{logs}

ROOT CAUSE ANALYSES:
{root_causes}

CHAOS RESULTS:
{chaos_results}

DEVELOPER QUESTION:

{question}

Rules:

- Be technically accurate.
- Use evidence from the application.
- If the evidence does not answer the question,
  say so.
- Do not fabricate source-code details.
- Give actionable engineering advice.
- Mention exact files/functions/lines when available.
"""


# =========================================================
# PROMPT BUILDERS
# =========================================================

def build_root_cause_prompt(
    project_map,
    failure_evidence,
    logs=None,
    stack_trace=None,
    chaos_result=None
):

    return ROOT_CAUSE_PROMPT.format(

        project_map=project_map,

        failure_evidence=failure_evidence,

        logs=logs or "No logs provided.",

        stack_trace=(
            stack_trace
            or "No stack trace provided."
        ),

        chaos_result=(
            chaos_result
            or "No chaos experiment result provided."
        )
    )


# =========================================================
# ARCHITECTURE PROMPT BUILDER
# =========================================================

def build_architecture_prompt(
    project_map
):

    return ARCHITECTURE_PROMPT.format(

        project_map=project_map

    )


# =========================================================
# CHAOS PROMPT BUILDER
# =========================================================

def build_chaos_prompt(
    project_map,
    experiment,
    result
):

    return CHAOS_ANALYSIS_PROMPT.format(

        project_map=project_map,

        experiment=experiment,

        result=result

    )


# =========================================================
# FIX PROMPT BUILDER
# =========================================================

def build_fix_prompt(
    root_cause,
    failure_location,
    evidence,
    code
):

    return FIX_PROMPT.format(

        root_cause=root_cause,

        failure_location=failure_location,

        evidence=evidence,

        code=code

    )


# =========================================================
# AI ENGINEER PROMPT BUILDER
# =========================================================

def build_ai_engineer_prompt(
    question,
    project_map=None,
    failures=None,
    logs=None,
    root_causes=None,
    chaos_results=None
):

    return AI_ENGINEER_PROMPT.format(

        project_map=(
            project_map
            or "No project map available."
        ),

        failures=(
            failures
            or "No failures available."
        ),

        logs=(
            logs
            or "No logs available."
        ),

        root_causes=(
            root_causes
            or "No root-cause analyses available."
        ),

        chaos_results=(
            chaos_results
            or "No chaos results available."
        ),

        question=question

    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 65)
    print("              CHAOSPILOT PROMPT SYSTEM")
    print("=" * 65)

    prompt = build_root_cause_prompt(

        project_map={
            "files": [
                "database.py",
                "payment.py"
            ]
        },

        failure_evidence={
            "exception": {
                "type": "ConnectionError",
                "message": "Database unavailable"
            }
        },

        logs=[
            "ERROR Database connection timeout"
        ],

        stack_trace=(
            'File "database.py", line 42, '
            'in connect_database'
        )

    )

    print()
    print(prompt)

    print()
    print("=" * 65)