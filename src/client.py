import os
from google.cloud import dialogflow
from ApiHandler import *
from rich.table import Table
from rich.console import Console

console = Console()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='../skylar-366108-9e5bcbd4a68c.json'
LANGUAGE_CODE = "en"


if __name__ == "__main__":
    user_name = input("Skylar: Hey there 👋 Please enter your name: ")

    print(f"Skylar: Hi {user_name}, I am an AI-powered chatbot using the Skyscanner API and natural language "
          f"processing to assist in finding the right flight for you.")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path('skylar-366108', 1)

    while True:
        user_text = input(f"{user_name}: ")
        text_input = dialogflow.TextInput(text=user_text, language_code=LANGUAGE_CODE)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("Skylar: " + response.query_result.fulfillment_text)
        context_name = response.query_result.intent.display_name

        all_values = {}
        for context in response.query_result.output_contexts:
            # A context is a map containing the input values
            if context.parameters:
                for key in list(context.parameters.keys()):
                    all_values[key] = context.parameters.get(key)

        filtered_values = {}
        for key in list(all_values.keys()):
            value = all_values.get(key)
            if isinstance(value, str):
                #Ignore these two original responses to get the mapped dates correctly
                if key != 'departure.original' and key != 'return.original' and key != 'currency.original':
                    try: 
                        if key.index('.original'):
                            #Remove .original from key
                            key = key[:-9]
                    except ValueError:
                        pass
                    filtered_values[key] = value

        sort_order_param = filtered_values.get('sort-order')
        currency = filtered_values.get('currency')
        adults = filtered_values.get('adult')
        children = filtered_values.get('child')
        from_date = filtered_values.get('departure')
        return_date = filtered_values.get('return')
        cabin_class = filtered_values.get('class')

        if context_name == 'flight.book - show-flight':
            all_flights, legs, carriers, sortingOptions, agents = fetchFlights(filtered_values.get('from'), filtered_values.get('to'), currency=currency, adults=adults, children=children, from_date=from_date, return_date=return_date, cabin_class=cabin_class)

            flight_list = []
            for sort in sortingOptions.get(sort_order_param):
                used_legs = list(map(lambda it: legs.get(it), all_flights.get(sort.get('itineraryId')).get('legIds')))

                pricing_options = list(map(lambda p: {'price': p.get('price'), 'agendIds': list(map(lambda aId: agents.get(aId).get('name'), p.get('agentIds')))}, all_flights.get(sort.get('itineraryId')).get('pricingOptions')))
                for leg in used_legs:
                    found_flight = {}
                    found_flight['departureDateTime'] = leg.get('departureDateTime')
                    found_flight['arrivalDateTime'] = leg.get('arrivalDateTime')
                    found_flight['durationInMinutes'] = leg.get('durationInMinutes')
                    found_flight['stopCount'] = leg.get('stopCount')
                    found_flight['operatingCarrierIds'] = list(map(lambda cId: carriers.get(cId).get('name'), leg.get('operatingCarrierIds')))
                    found_flight['pricingOptions'] = pricing_options
                    
                    flight_list.append(found_flight)

            # Get price list:
            #list(map(lambda f: list(map(lambda p: p.get('price').get('amount'), f.get('pricingOptions'))), flight_list))
            top_ten_results = flight_list[0:10]

            table = Table(show_header=True, header_style='bold yellow')
            table.add_column('Price')
            table.add_column('Stop Count')
            table.add_column('Duration')
            table.add_column('Airline(s)')
            table.add_column('Departure Date')
            table.add_column('Departure Time')
            table.add_column('Arrival Date')
            table.add_column('Arrival Time')
            
            get_date = lambda d: "{0:0>2}".format(d.get('day')) + '.' + "{0:0>2}".format(d.get('month')) + '.' + str(d.get('year'))
            get_time = lambda d: "{0:0>2}".format(d.get('hour')) + ':' + "{0:0>2}".format(d.get('minute'))

            for row in top_ten_results:
                duration_hours = int(row.get('durationInMinutes') / 60)
                duration_minutes = row.get('durationInMinutes') % 60
                duration_text = str(duration_hours) + 'h' + str(duration_minutes) + 'min'
                price = '\n or '.join(list(map(lambda po: str(int(po.get('price').get('amount') or 0) / 1000) + ' ' + currency + ' on ' + str(po.get('agendIds')), row.get('pricingOptions'))))
                departureDate = get_date(row.get('departureDateTime'))
                departureTime = get_time(row.get('departureDateTime'))
                operatingCarrierIds = row.get('operatingCarrierIds')
                arrivalDate = get_date(row.get('arrivalDateTime'))
                arrivalTime = get_time(row.get('arrivalDateTime'))
                stopCount = row.get('stopCount')
                table.add_row(f'[red]{price}', f'[red]{stopCount}', f'[magenta]{duration_text}', f'[magenta]{operatingCarrierIds}', f'[yellow]{departureDate}', f'[yellow]{departureTime}', f'[blue]{arrivalDate}', f'[blue]{arrivalTime}')
            console.print(table)
