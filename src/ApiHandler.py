import requests
from dateutil import parser

API = "https://partners.api.skyscanner.net/apiservices/v3/"
KEY_HEADER = {"x-api-key": "prtl6749387986743898559646983194"}
# "CABIN_CLASS_UNSPECIFIED", "CABIN_CLASS_ECONOMY", "CABIN_CLASS_PREMIUM_ECONOMY", "CABIN_CLASS_BUSINESS", "CABIN_CLASS_FIRST"
CABIN_CLASS = "CABIN_CLASS_ECONOMY" 

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

def fetchFlights(originIATA, destinationIATA, currency, adults, children, from_date, return_date, cabin_class):
    from_date_parsed = parser.parse(from_date)

    response = requests.post(API + "flights/live/search/create", headers=KEY_HEADER, json={
        "query": {
        "market": "CH",
        "locale": "de-DE",
        "currency": currency,
        "queryLegs": [
            {
                "date": {
                    "day": from_date_parsed.day,
                    "month": from_date_parsed.month,
                    "year": from_date_parsed.year
                },
                "originPlaceId": {
                    "iata": originIATA.upper()
                },
                "destinationPlaceId": {
                    "iata": destinationIATA.upper()
                }
            }
        ],
        "groupPricing": False, # show price per person
        "adults": adults,
        "children": children, # 1-16 years
        "infants": 0, # 0-12 months
        "childrenAges": [],
        "cabinClass": cabin_class,
        "excludedAgentsIds": [],
        "excludedCarriersIds": [],
        "includedAgentsIds": [],
        "includedCarriersIds": [], # IATA code of airlines
        "includeSustainabilityData": False # Eco data
    }
    })
    content = response.json()
    if response.status_code != 200 or content.get("status") == "RESULT_STATUS_FAILED":
        raise Exception("Could not load flights")
    else:
        return content.get("content").get("results").get("itineraries"), content.get("content").get("results").get("legs"), content.get("content").get("results").get("carriers"), content.get("content").get("sortingOptions"), content.get("content").get("results").get("agents")


if __name__ == "__main__":
    currencies = fetchFlights("ZRH", "LAX", "CHF", 2)
    print(currencies)