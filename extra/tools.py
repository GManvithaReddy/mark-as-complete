from datetime import datetime
import json
import requests
from requests.auth import HTTPBasicAuth
from .state import State

class LoadTracker:
    def __init__(self):
        self.processed_loads = set()  # Initialize an empty set to track processed load numbers

    def check_load_details_and_update(self, state: State):
        load_numbers_to_process = []
        timestamps_to_process = []

        for timestamp, load_number in zip(state["timestamps"], state["load_numbers"]):
            if load_number in self.processed_loads:
                continue  # Skip if load_number has already been processed

            load_numbers_to_process.append(load_number)
            timestamps_to_process.append(timestamp)
            self.processed_loads.add(load_number)  # Mark load number as processed

        if not load_numbers_to_process:
            print("No new loads to process.")
            return state

        # Convert timestamps to ISO strings
        iso_strings = [datetime.strptime(ts, "%m/%d/%Y %H:%M:%S").isoformat() for ts in timestamps_to_process]

        get_load_url = 'https://tracking-api-qat.fourkites.com/api/v1/tracking/search?company_id=test-shipper-2'
        payload = json.dumps({
            "load_ids": load_numbers_to_process
        })

        headers = {
            'Content-Type': 'application/json',
        }

        try:
            # Make a single API request for all load numbers
            load_response = requests.get(get_load_url, auth=HTTPBasicAuth('manvitha.g@fourkites.com', 'Manutanu*1309'), data=payload)

            if load_response.status_code == 200:
                load_data = load_response.json().get("loads", [])
                for load in load_data:
                    tracking_id = load["id"]
                    stop_id = load["originStopId"]
                    state["tracking_ids"].append(tracking_id)
                    state["stop_ids"].append(stop_id)
                    state["iso_strings"].append(iso_strings.pop(0))  # Use each ISO string in sequence
                    self.update_status(tracking_id, stop_id, state["iso_strings"][-1])  # Update status for each load

                    # Add the load_number to processed loads set
                    self.processed_loads.add(load["loadNumber"])
            else:
                print(f"Failed to fetch data. Status code: {load_response.status_code}")

        except requests.RequestException as e:
            print(f"Request failed: {e}")

        return state

    def update_status(self, tracking_id, stop_id, iso_string):
        post_load_url = f'https://tracking-api-qat.fourkites.com/api/v1/tracking/{tracking_id}/stops/{stop_id}/mark_as_completed?locale=en'
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            "arrivalTime": iso_string,
            "departureTime": iso_string
        }

        try:
            response = requests.post(post_load_url, auth=HTTPBasicAuth('manvitha.g@fourkites.com', 'Manutanu*1309'), json=data)
            if response.status_code == 200:
                print('Form submitted successfully:', response.json())
            else:
                print('Failed to submit form:', response.status_code, response.text)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
