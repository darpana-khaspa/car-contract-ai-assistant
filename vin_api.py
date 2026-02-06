import requests

def fetch_vehicle_details(vin):
    """
    Fetch vehicle details from NHTSA VIN Decode API
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return {"error": "Failed to fetch vehicle details"}

    data = response.json()
    results = data.get("Results", [])

    vehicle_info = {}
    for item in results:
        if item["Value"]:
            vehicle_info[item["Variable"]] = item["Value"]

    return vehicle_info