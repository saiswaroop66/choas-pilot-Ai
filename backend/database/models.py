from dataclasses import dataclass
from typing import Optional


@dataclass
class User:

    id: Optional[int] = None

    name: str = ""

    email: str = ""

    password: str = ""


@dataclass
class Application:

    id: Optional[int] = None

    user_id: Optional[int] = None

    name: str = ""

    description: str = ""

    repository: str = ""

    environment: str = "development"

    status: str = "active"


@dataclass
class Analysis:

    id: Optional[int] = None

    application_id: Optional[int] = None

    analysis_type: str = ""

    result: str = ""


@dataclass
class Failure:

    id: Optional[int] = None

    application_id: Optional[int] = None

    component: str = ""

    severity: str = ""

    file_name: str = ""

    function_name: str = ""

    line_number: Optional[int] = None

    root_cause: str = ""

    impact: str = ""

    recommendation: str = ""


@dataclass
class Experiment:

    id: Optional[int] = None

    application_id: Optional[int] = None

    experiment_name: str = ""

    failure_type: str = ""

    status: str = "pending"

    result: str = ""


@dataclass
class Report:

    id: Optional[int] = None

    application_id: Optional[int] = None

    title: str = ""

    content: str = ""

    resilience_score: Optional[int] = None