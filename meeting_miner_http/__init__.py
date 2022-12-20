import logging

import azure.functions as func

import json

import datetime

import os

# Third party libraries
from io import StringIO
import base64
# import tempfile
# from os import listdir
# from transformers import pipeline


# Helper functions
from shared_code.helper_functions import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:

        req_body = req.get_body()
        # print(f"BODY: { req_body[:500] }")

        transcript_bytes = base64.b64decode(req_body + b'==')
        transcript_text = transcript_bytes.decode('utf-8')
        # print(f"TRANSCRIPT: { transcript_text[:500] }")

        # Take transcript file text input (from Power Automate) and construct an input to webvtt
        transcript_text_buffer = StringIO(transcript_text)

        # Store transcript in temporary VTT file 
        # tempFilePath = tempfile.gettempdir()
        # fp = tempfile.NamedTemporaryFile(suffix='.vtt')
        # fp.write(transcript_bytes)
        # file_name = fp.name
        # print(listdir(tempFilePath))
        
        # Construct the parsed conversation object
        convo = parse_vtt_data(transcript_text_buffer)

        # Score the conversation items as follow-up/not via the LUIS endpoint URL
        # luis_endpoint_url = "https://luis-for-followup-recognition.cognitiveservices.azure.com/luis/prediction/v3.0/apps/d72eaca3-1cff-49ed-b769-fce7c6c71805/slots/staging/predict?verbose=true&show-all-intents=true&log=true&subscription-key=51f33a9b20bd4f1da87e0af8c5fc64b7&query="
        # intents_list = score_conversation(convo, luis_endpoint_url)

        # Format scored items as a dataframe. Filter out follow-ups. 
        df = build_df(convo)
        # followup_intents_df = df[ (df['top_intent'] == 'followUp') ]
        # json_obj_list = [] # Format needed to create HTML table in Power Automate
        # for _, row in followup_intents_df.iterrows():
        #     json_obj_list.append({'who': row['who'], 'what': row['what'], 'when': row['when']}) # TODO: Include recognized entities. 

        # Get general metrics about the meeting from the data. Who attended, meeting length, etcetera.
        general_meeting_metrics = extract_meeting_general_metrics(df)
        # print("GENERAL METRICS:\n\n ", general_meeting_metrics)

        # Format transcript into one big chunk, then smaller chunks that can be passed to GPT-3.
        aggregated_transcript = aggregate_transcript(convo, compress_w_gpt3=False)

        # Summarize the transcript with GPT-3.
        summary = summarize_transcript(aggregated_transcript)
        # summarizer = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")
        # summary = summarizer(aggregated_transcript)

        # print("\n\nSUMMARY:\n\n", summary)

        followups = identify_followups(aggregated_transcript)
        followups_list = followups.split('; ')

        print(followups_list)

        # Store in development to a local directory for comparison.
        if not bool(int(os.environ["PRODUCTION"])):	
            timestamp = str(datetime.datetime.now()).replace(' ', '_').replace(':','_')
            file_path = f"local_test_files/summary_at_{timestamp}.txt"
            with open(file_path, "w") as text_file:
                text_file.write(f"Transcript start: {aggregated_transcript[0][:500]} \n\n" + "Summary:\n\n" + summary + \
                                  "\n\n" + "Follow-ups:\n\n" + followups)

        # RETURN: Object. Attr.s: (1) Formatted *list* of follow-ups, (2) Meeting summary *string*
        return func.HttpResponse (
                json.dumps({
                    'action_items': followups_list,
                    'meeting_summary': summary,
                    'general_meeting_metrics': general_meeting_metrics
                }) 
            )
    except Exception as e:
        return func.HttpResponse(
                f"An exception occurred in the execution of this function. Exception: {e}.",
                status_code=500
        )
"""
# Starter code
name = req.params.get('name')
if not name:
    try:
        req_body = req.get_json()
    except ValueError:
        pass
else:
    name = req_body.get('name')

if name:
    return func.HttpResponse(f"Hellooo, {name}. This HTTP triggered function executed successfully.")
else:
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
"""
