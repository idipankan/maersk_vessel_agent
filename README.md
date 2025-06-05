# Maersk Vessel Deadline Agent

A Google Agent Development Kit (ADK) application that provides information about Maersk vessel deadlines for specific voyages. This agent helps users retrieve vessel information and shipment deadlines using the Maersk API.

## Features

- Retrieve vessel IMO numbers using vessel names
- Get detailed shipment deadlines for specific voyages
- Automatic country code inference from country names
- Integration with Maersk's API for real-time vessel information

## Prerequisites

- Python 3.11 or higher
- Google ADK (Agent Development Kit)
- Maersk API access credentials

## Usage

The agent provides two main functionalities:

### 1. Get Vessel Information
```python
from agent import get_vessel_info

# Get IMO number for a vessel
imo_number = get_vessel_info("MAERSK SEVILLE")
```

### 2. Get Vessel Deadlines
```python
from agent import get_vessel_deadlines

# Get deadlines for a specific voyage
deadlines = get_vessel_deadlines(
    iso_country_code="US",
    port_of_load="NEW YORK",
    vessel_imonumber="1234567",
    voyage="123E"
)
```

## API Parameters

### get_vessel_info
- `vessel_name` (str): Name of the Maersk vessel

### get_vessel_deadlines
- `iso_country_code` (str): ISO 3166-1 alpha-2 country code
- `port_of_load` (str): Name or code of the loading port
- `vessel_imonumber` (str): IMO number of the vessel
- `voyage` (str): Voyage identifier for the sailing

## Response Format

The `get_vessel_deadlines` function returns a dictionary with the following structure:

```python
{
    "status": "success" | "error",
    "report": "Human-readable summary of deadlines",  # Only present if status is "success"
    "error_message": "Error message"  # Only present if status is "error"
}
```

## Demonstration screenshots

When the parameters are directly provided for, the tool decides to retrieve the relevant details:
![alt text](https://idipankan.com/wp-content/uploads/2025/06/maersk-ADK.png)

However, when the request is more complex, it intelligently utilizes the vessel name to IMO Number decoder tool and then proceeds to fetch the data.
![alt text](https://idipankan.com/wp-content/uploads/2025/06/maersk-ADK-2.png)
