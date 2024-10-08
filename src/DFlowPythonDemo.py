import os
from google.cloud import dialogflow

# path to the key-file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='../skylar-366108-9e5bcbd4a68c.json'


# example from  https://cloud.google.com/dialogflow/es/docs/quick/api#detect-intent-text-python
def detect_intent_demo(project_id, session_id, texts, language_code):
    """
    https://cloud.google.com/dialogflow/es/docs/quick/api#detect-intent-text-python

    Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text)) # Set a breakpoint here and look at variables in debugger

if __name__ == "__main__":
    # change the values accordingly
    detect_intent_demo('skylar-366108', '1', ['yes'], 'en')