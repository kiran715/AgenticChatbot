from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from typing import Annotated, List
from typing_extensions import TypedDict

class State(TypedDict):
    """
    Represent the structure of the state used in Graph
    """
    messages: Annotated[List, add_messages]