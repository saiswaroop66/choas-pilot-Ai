from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai.agent import ChaosPilotAgent


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/ai-engineer",
    tags=["AI Engineer"]
)


# =========================================================
# CHAOSPILOT AGENT
# =========================================================

agent = ChaosPilotAgent()


# =========================================================
# CHAT REQUEST
# =========================================================

class AIChatRequest(BaseModel):

    application_id: int

    message: str

    context: Optional[str] = None

    project_map: Optional[Any] = None

    failures: Optional[Any] = None

    logs: Optional[Any] = None

    root_causes: Optional[Any] = None

    chaos_results: Optional[Any] = None


# =========================================================
# CHAT ENDPOINT
# =========================================================

@router.post("/chat")
def chat(
    data: AIChatRequest
):

    if not data.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    question = data.message.strip()

    if data.context:

        question = f"""
Application context:

{data.context}

Developer question:

{question}
"""

    try:

        result = agent.ask(

            question=question,

            project_map=data.project_map,

            failures=data.failures,

            logs=data.logs,

            root_causes=data.root_causes,

            chaos_results=data.chaos_results

        )

        return {

            "success": True,

            "application_id":
                data.application_id,

            "question":
                data.message,

            "response":
                result.get(
                    "response",
                    ""
                )

        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=f"AI Engineer failed: {error}"

        )


# =========================================================
# COMPLETE ANALYSIS REQUEST
# =========================================================

class AnalyzeRequest(BaseModel):

    application_id: int

    failure: Any

    project_map: Optional[Any] = None

    logs: Optional[Any] = None

    stack_trace: Optional[str] = None

    chaos_result: Optional[Any] = None

    dependencies: Optional[Any] = None

    call_graph: Optional[Any] = None


# =========================================================
# COMPLETE CHAOSPILOT ANALYSIS
# =========================================================

@router.post("/analyze")
def analyze(
    data: AnalyzeRequest
):

    try:

        result = agent.analyze(

            failure=data.failure,

            project_map=data.project_map,

            logs=data.logs,

            stack_trace=data.stack_trace,

            chaos_result=data.chaos_result,

            dependencies=data.dependencies,

            call_graph=data.call_graph

        )

        return {

            "success": True,

            "application_id":
                data.application_id,

            "status":
                result.get(
                    "status",
                    "completed"
                ),

            "report":
                result.get(
                    "report",
                    {}
                )

        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                f"ChaosPilot analysis failed: "
                f"{error}"
            )

        )


# =========================================================
# AI HEALTH
# =========================================================

@router.get("/health")
def health():

    try:

        llm = agent.reasoner.llm

        configured = llm.is_configured()

        model = llm.get_model()

        return {

            "success": True,

            "service":
                "ChaosPilot AI",

            "provider":
                "Groq",

            "model":
                model,

            "configured":
                configured,

            "status":
                "ready"
                if configured
                else "not_configured"

        }

    except Exception as error:

        return {

            "success": False,

            "service":
                "ChaosPilot AI",

            "status":
                "error",

            "error":
                str(error)

        }
