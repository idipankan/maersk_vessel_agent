from google.adk.agents import Agent
import requests
import dotenv   
import os

dotenv.load_dotenv()

header = {"Consumer-Key": os.getenv("CONSUMER_KEY")} # Maersk consumer API Key

def get_vessel_info(vessel_name: str):
    """
        Retrieves the IMO number of a Maersk vessel.

        Args:
            vessel_name (str): Name of the vessel.

        Returns:
            str: IMO number of the vessel.
    """
    url = f"https://api.maersk.com/reference-data/vessels?vesselNames={vessel_name}"
    response = requests.get(url, headers=header)
    data = response.json()
    return data[0]["vesselIMONumber"]


def get_vessel_deadlines(iso_country_code: str, port_of_load: str, vessel_imonumber: str, voyage: str):
    """
        Retrieves shipment deadlines for a specific Maersk vessel voyage.

        Args:
            iso_country_code (str): ISO 3166-1 alpha-2 country code of the port of load.
            port_of_load (str): Name or code of the loading port.
            vessel_imonumber (str): IMO number of the vessel.
            voyage (str): Voyage identifier for the sailing.

        Returns:
            dict: A dictionary with:
                - "status": "success" or "error"
                - "report": Human-readable summary of deadlines (if successful)
                - "error_message": Error message (if no data is found)
    """

    url = f"https://api.maersk.com/shipment-deadlines?ISOCountryCode={iso_country_code}&portOfLoad={port_of_load}&vesselIMONumber={vessel_imonumber}&voyage={voyage}"
    response = requests.get(url, headers=header)
    data = response.json()

    if len(data) == 0:
        return {
            "status": "error",
            "error_message": f"No data found for the given parameters.",
        }

    terminal_name = data[0]["shipmentDeadlines"]["terminalName"]
    deadlines_joined = ", ".join(f'{deadline["deadlineName"]} on {deadline["deadlineLocal"]}' for deadline in data[0]["shipmentDeadlines"]["deadlines"])

    return {
        "status": "success",
        "report": f"The vessel {vessel_imonumber} is scheduled to arrive at {terminal_name} with deadlines: {deadlines_joined}.",
    }



root_agent = Agent(
    name="vessel_deadline_agent",
    model="gemini-2.0-flash-lite",
    description=(
        "Agent to answer questions about the deadlines of a Maersk vessel for a given voyage."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the deadlines of a Maersk vessel for a given voyage, given the following parameters: ISO country code, port of load, vessel IMO number, and voyage."
        "You can use the following tools to answer the user's question:"
        "- get_vessel_info: to get the IMO number of a Maersk vessel, in case a vessel name is provided instead of an IMO number."
        "- get_vessel_deadlines: to get the deadlines of a Maersk vessel for a given voyage. This has to be sequentially called after obtaining the IMO number of the vessel."
        "If the ISO Country code is not provided, infer the country code from the Country Name."
    ),
    tools=[get_vessel_info, get_vessel_deadlines],
)
