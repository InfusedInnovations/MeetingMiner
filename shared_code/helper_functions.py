
# Third-party libraries
import openai
import requests
import pandas
from shared_code.custom_webvtt import WebVTT
import urllib.parse
import json
import time
import copy
import timeit
import math
import os
import datetime

def parse_speaker_from_vtt_tag(tag):
  """Returns the name of the speaker given a tag from a VTT file."""
  return tag[0].split('>')[0][2:][1:]


def parse_vtt_data(string_buffer):
  """
  Take in VTT file and return an object containg the who, what and when.
  """
  meeting_convo = {
      'who': [],  # Who spoke.
      'what': [], # What they said.
      'when': []  # When they said it. Each item is a tuple of: (start time, end time)
  }

  # Caption object looks like:
  """
  ['CUE_TEXT_TAGS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
  '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
  '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
  '__weakref__', '_clean_cue_tags', '_end', '_lines', '_parse_timestamp', '_start', '_to_seconds', '_to_timestamp', 'add_line',
  'end', 'end_in_seconds', 'identifier', 'lines', 'raw_text', 'start', 'start_in_seconds', 'text']
  """

  for caption in WebVTT().read_buffer(string_buffer):
    meeting_convo['who'].append( parse_speaker_from_vtt_tag(caption._lines) )
    meeting_convo['what'].append( caption.text )
    meeting_convo['when'].append( (caption.start, caption.end) )
    
  return meeting_convo


def parse_vtt_data_filename(filename):
  """
  Take in VTT file and return an object containg the who, what and when.
  """
  meeting_convo = {
      'who': [],  # Who spoke.
      'what': [], # What they said.
      'when': []  # When they said it. Each item is a tuple of: (start time, end time)
  }

  # Caption object looks like:
  """
  ['CUE_TEXT_TAGS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
  '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
  '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
  '__weakref__', '_clean_cue_tags', '_end', '_lines', '_parse_timestamp', '_start', '_to_seconds', '_to_timestamp', 'add_line',
  'end', 'end_in_seconds', 'identifier', 'lines', 'raw_text', 'start', 'start_in_seconds', 'text']
  """

  for caption in WebVTT().read(filename):
    meeting_convo['who'].append( parse_speaker_from_vtt_tag(caption._lines) )
    meeting_convo['what'].append( caption.text )
    meeting_convo['when'].append( (caption.start, caption.end) )
    
  return meeting_convo


def reconstruct_data(convo, index, intents_list=None):
  """
  Takes in an index and returns that row of data.
  If a list of intents is included, return the intent of this row.
  """
  speaker, said, time, top_intent = convo['who'][index], convo['what'][index], convo['when'][index], intents_list[index] if intents_list else None
  return {'speaker':speaker, 'said':said, 'time':time, 'top_intent': top_intent}


def score_conversation(convo_obj, luis_endpoint_url):
  """
  Take in an object that describes the tokenized conversation and
  return a list of intents scored by LUIS.
  """
  intents_list = []

  # start_time = timeit.default_timer()
  # calls_since_last_sleep = 0

  # Pass each passafe to the LUIS endpoint to determine its intent and store.
  for counter, passage in enumerate(convo_obj['what']):

    # print(counter)

    # current_time = timeit.default_timer()
    # time_since_last_sleep = current_time - start_time
    # if (time_since_last_sleep > 0.7) and (calls_since_last_sleep == 5): # In current pricing tier, need to wait so as to not exceed API rate limit. 5 allowed per second.
    #   # print('Pause')
    #   time.sleep(1.1 - time_since_last_sleep) # So, if 5 calls made, sleep for the rest of this second. Using 1.1s to maintain a buffer.
    #   calls_since_last_sleep = 0 # Since slept, reset calls since last sleep.
    #   start_time = timeit.default_timer() # Reset start time.

    # time.sleep(0.21)

    # Make a call to the LUIS endpoint.
    # print(passage)
    query = urllib.parse.quote(passage)[0:500] # Query cannot exceed 500 characters. Split in halves until the parts meet criteria?
    url = luis_endpoint_url + query
    # print(url)
    luis_response = json.loads(requests.get(url).text) # NOTE: Will want to parse entities from this response as well.
    # print(luis_response)
    prediction_obj = {}
    try:
      top_intent = luis_response['prediction']['topIntent']
      prediction_obj = { 'topIntent': top_intent, 'score': luis_response['prediction']['intents'][top_intent]['score'], 'entities': luis_response['prediction']['entities']}
    except Exception as e:
      print(e)
      print(luis_response)

    intents_list.append(prediction_obj)

    # Note that the endpoint was called. Used for avoiding rate limit.
    # calls_since_last_sleep += 1

  return intents_list


def extract_meeting_general_metrics(convo_df):
  """
  Extract general metrics about the meeting such as the list of people involved and
  the length of the meeting.
  """

  general_metrics = {
    'attendees': list(convo_df['who'].unique()),
    'attendees_str': ', '.join(list(convo_df['who'].unique())),
    'meeting_length': tuple(convo_df['when'].iloc[-1])[1].split('.')[0], # The second element of the 'when' tuple (end time) up to the time in seconds
  }

  return general_metrics




def build_df(convo, intents_list=None):
  """
  Turn parsed conversation data and scores into a dataframe for reading as a table/manipulation.
  """
  pre_df_dict = copy.deepcopy(convo)
  if intents_list:
    pre_df_dict.update({
        'top_intent':[i['topIntent'] for i in intents_list],
        'score': [i['score'] for i in intents_list],
        'entities': [str(i['entities']) for i in intents_list]
    })
  df = pandas.DataFrame.from_dict(pre_df_dict)

  # Output dataframe to file in development environment.
  if not bool(int(os.environ["PRODUCTION"])):	  
    timestamp = str(datetime.datetime.now()).replace(' ', '_').replace(':','_')
    file_path = f"local_test_files/summary_at_{timestamp}.txt"
    with open(file_path, "w") as text_file:
      text_file.write(f"All item scores CSV: \n\n")

    df.to_csv(file_path, mode='a', index=False, header=True)

  return df


def aggregate_transcript(convo, compress_w_gpt3=False):
  """
  Aggregate the transcript and compress pieces where necessary.
  compress_w_gpt3: Do an intermediate compression stage on transcript parts using GPT3.
  """

  openai.api_key = "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"

  aggregated_transcript = [""]

  # sum_len_transcript_parts = 0 # Use to sum up the total transcript length and split it into parts when necessary.
  for counter, _ in enumerate(convo['what']):

    what = convo['what'][counter]
    # orig_what = what # Store for comparison
    # summarized = False

    # IMPORTANT: Want to limit the amount of compression/information loss here. Meeting transcripts that become very long should be split into multiple parts and each part summarized.
    # NOTE: There might be ways to bypass the token length limit of the GPT-3 model.

    len_transcript_item = len(what.split(" "))
    # sum_len_transcript_parts += len_transcript_item
    if len(aggregated_transcript[-1].split(" ")) > 2000: # If transcript getting too long for GPT-3...
        aggregated_transcript.append("")  # Split it into another part.
        # sum_len_transcript_parts = 0

    if compress_w_gpt3:
      if len_transcript_item > 60: # More than N words in the transcript item.
        what_obj = openai.Completion.create(
          engine="text-davinci-003",
          prompt=f"Summarize the following text:\n\n{convo['what'][counter]}",
          temperature=0.0,
          max_tokens=60,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        # print(what_obj)
        what = what_obj["choices"][0]["text"]
        summarized = True

    # if summarized:
    #   print("ORIG: ", orig_what)
    #   print("FINAL: ", what)

    aggregated_transcript[-1] += convo['who'][counter].split(' ')[0] + ": " + what + "\n"

  return aggregated_transcript


def summarize_transcript(aggregated_transcript):

  summarized_transcript = ""

  final_summary_len = 1/15 # Size of the transcript summary in proportion to original length.

  for transcript_part in aggregated_transcript:
    # print(transcript_part)
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"""Convert the meeting transcript into a kind and professional first-hand summary of the meeting:
                Transcript 1:

                Mary Adams: Hi Mike!
                Mike Daly: Hello.
                Mary Adams: do u have any plans for tonight?
                Mike Daly: I'm going to visit my grandma.
                Mike Daly: You can go with me.
                Mike Daly: She likes u very much.
                Mary Adams: Good idea, i'll buy some chocolate for her.
 
                Summary 1:

                Mike and Mary discussed going to visit Mike's grandma tonight. Mary will buy Mike's grandma some chocolate.

                Transcript 2:
                {transcript_part}
                
                Summary 2:""",
      temperature=0.0,
      max_tokens=math.ceil(len(transcript_part.split(" ")) * final_summary_len),
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    summarized_transcript += response['choices'][0]['text'] 

  return summarized_transcript


def identify_followups(aggregated_transcript):
  """
  Use GPT-3 to identify action items from the meeting transcript.
  """
  transcript_followups = ""

  final_summary_len = 1/20 # Size of the transcript summary in proportion to original length.

  for transcript_part in aggregated_transcript:
    # print(transcript_part)
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"""Convert the meeting transcript into a kind and professional list of action items:
                Transcript 1:

                Mary Adams: Hi Mike!
                Mike Daly: Hello.
                Mary Adams: do u have any plans for tonight?
                Mike Daly: I'm going to visit my grandma.
                Mike Daly: You can go with me.
                Mike Daly: She likes u very much.
                Mary Adams: Good idea, i'll buy some chocolate for her.
 
                Action items for transcript 1:

                *Mary will buy some chocolate for Mike's grandma.*

                *Mike and Mary will travel to Mike's grandmother's together.*

                Transcript 2:
                {transcript_part}
                
                Action items for transcript 2:""",
      temperature=0.0,
      max_tokens=math.ceil(len(transcript_part.split(" ")) * final_summary_len),
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    transcript_followups += response['choices'][0]['text'] 

  return transcript_followups