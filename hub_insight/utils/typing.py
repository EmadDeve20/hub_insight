from typing import TypedDict, Optional

class JobDetail(TypedDict):
    help: str
    name: str
    version: str = "v1"


class JobVariable(TypedDict):
    name :str
    variable_type: type
    default: Optional[type]


class JobReturnAnnotation(TypedDict):
    return_type: type

