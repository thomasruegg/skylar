import os
from google.cloud import dialogflow
from ApiHandler import *

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
                if key != 'departure.original' and key != 'return.original':
                    try: 
                        if key.index('.original'):
                            #Remove .original from key
                            key = key[:-9]
                    except ValueError:
                        pass
                    filtered_values[key] = value



        if context_name == 'flight.book - payment':
            print(fetchFlights(filtered_values.get('from'), filtered_values.get('to'), "CHF", 2))


