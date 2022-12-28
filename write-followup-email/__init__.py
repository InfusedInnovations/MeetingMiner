import logging
import openai
import json
import azure.functions as func
import os

openai.api_key = "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"


def write_followup_email(meeting_summary, action_items):
    """Write a follow-up email to the meeting attendees."""

    response = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=512,
        prompt=
        f"""
        Write a professional and succinct follow-up email to the customer using the summary and action items as context.

        Summary: 

        { meeting_summary }

        Action items:
        
        { action_items }

        Follow-up email:"""
    )

    email_body = response.choices[0].text

    return email_body

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # TODO: Accept input = meeting summary and action items.

        req_body = req.get_json()
        summary, action_items = req_body.get('summary'), req_body.get('action_items')

        # TODO: Feed input to GPT-3 to generate a follow-up email.
        email_body = write_followup_email(summary, action_items)

        # if not bool(int(os.environ["PRODUCTION"])): # Log email body if not in production.
        print("Email body: " + email_body)

        # TODO: Return email body.
        return func.HttpResponse(
            json.dumps({'body': email_body})
        )

    except Exception as e:
        return func.HttpResponse(
                f"An exception occurred in the execution of this function. Exception: {e}.",
                status_code=500
        )