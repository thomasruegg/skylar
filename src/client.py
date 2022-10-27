import os
from google.cloud import dialogflow

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


