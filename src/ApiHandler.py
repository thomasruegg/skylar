import requests

API = "https://partners.api.skyscanner.net/apiservices/v3/"
KEY_HEADER = {"x-api-key": "prtl6749387986743898559646983194"}
LOCALE = "de-DE"
CABIN_CLASS = "CABIN_CLASS_ECONOMY" #"Economy", "PremiumEconomy", "Business", "First"

def fetchCurrencies(): 
    response = requests.get(API + "culture/currencies", headers=KEY_HEADER)
    content = response.json()
    if response.status_code != 200 or content.get("status", "") != "RESULT_STATUS_COMPLETE":
        raise Exception("Could not load currencies")
    else:
        return content.get("currencies", {})

def fetchAirports():
    response = requests.get(API + "geo/hierarchy/flights/" + LOCALE, headers=KEY_HEADER)
    content = response.json()
    if response.status_code != 200 or content.get("status", "") != "RESULT_STATUS_COMPLETE":
        raise Exception("Could not load airports")
    else:
        airport = {}
        for (key, value) in content.get("places", {}).items():
            if value.get("type", "") == "PLACE_TYPE_AIRPORT":
                airport[value.get("iata")] = value
        return airport

def fetchFlights(originIATA, destinationIATA, currecy, seats_num):
    response = requests.post(API + "flights/live/search/create", headers=KEY_HEADER, json={
        "query": {
        "market": "CH",
        "locale": LOCALE,
        "currency": currecy,
        "queryLegs": [
            {
                "originPlaceId": {
                    "iata": originIATA
                },
                "destinationPlaceId": {
                    "iata": destinationIATA
                },
                "date": {
                    "year": 2022,
                    "month": 10,
                    "day": 20
                    # "hour": 9
                }
            }
        ],
        "groupPricing": False, #show price per person
        "adults": seats_num,
        "children": 0, #1-16 years
        "infants": 0, #0-12 months
        "childrenAges": [],
        "cabinClass": "CABIN_CLASS_ECONOMY",
        "excludedAgentsIds": [],
        "excludedCarriersIds": [],
        "includedAgentsIds": [],
        "includedCarriersIds": []
    }
    })
    content = response.json()
    if response.status_code != 200 or content.get("status") == "RESULT_STATUS_FAILED":
        raise Exception("Could not load airports")
    else:
        return content.get("content").get("results").get("itineraries")


if __name__ == "__main__":
    currencies = fetchFlights("ZRH", "LAX", "CHF", 2)
    print(currencies)