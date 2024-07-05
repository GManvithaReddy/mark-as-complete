from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END

from .state import State
from .nodes import Nodes
from .tools import LoadTracker  # Adjusted import

class WorkFlow():
    def __init__(self):
        nodes = Nodes()
        load_tracker = LoadTracker()
        workflow = StateGraph(State)

        workflow.add_node("check_new_emails", nodes.check_email)
        workflow.add_node("extract_attachments", nodes.extract_attachments)
        workflow.add_node("extract_data", nodes.extract_data)
        workflow.add_node("check_load_details", load_tracker.check_load_details_and_update)  # Adjusted node reference

        workflow.set_entry_point("check_new_emails")
        workflow.add_edge("check_new_emails", "extract_attachments")
        workflow.add_edge("extract_attachments", "extract_data")
        workflow.add_edge("extract_data", "check_load_details")
        workflow.add_edge("check_load_details", END)  # Removed `update_status` node and linked to END
        
        self.app = workflow.compile()
