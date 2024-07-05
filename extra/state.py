from typing import TypedDict, List

class State(TypedDict):
    checked_emails_ids: List[str]
    emails: List[dict]
    action_required_emails: dict
    file_name: str
    timestamps: List[str]
    load_numbers: List[str]
    tracking_ids: List[str]
    stop_ids: List[str]
    iso_strings: List[str]

    