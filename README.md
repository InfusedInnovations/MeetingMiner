# MeetingMiner

<img src="/MM-logo.png" width="200px" height="200px" style="border-radius:50%" />

A GPT-based natural language cognitive assistant for extracting valuable information from Microsoft Teams meetings.
MeetingMiner can write follow-up emails to operationalize information, identifying action items to be shared with teammates, and more.

## Solution demonstration

A demonstration of the MeetingMiner solution can be found [here](https://www.figma.com/proto/B6nuI0whiPscjNVECBvpwr/MeetingMiner-Demo?node-id=180%3A298&scaling=scale-down&page-id=55%3A0&starting-point-node-id=180%3A298).

## Repository contents

This repository will contain all of the components needed to launch MeetingMiner as a solution in your enterprise. Infused Innovations will not pay for the operating costs of this solution which include, but are not limited to, API interactions with GPT, hosting in Azure, and Power Platform licensing.

The components include:

<!-- TODO: Create table with resource name, type and purpose for easy reading. -->

1. Power Platform solution (.zip) 
    * Power Automate flows for the purpose of
      - Subscring to Microsoft Graph events to receive webhook events when a meeting ends or begins.
      - Handling Microsoft Graph events when meeting ends to process the meeting transcript and store its outputs.
      - Handling meeting start events to remind a meeting's organizer to start transcribing the meeting.
    * Power Apps app (user interface)
    * Custom Datverse tables for this solution
2. Azure Function App
    * Hosts the OpenAI code for the A.I. to process meeting transcript data into more valuable outputs.
    * Contains a function which can be called to write a follow-up email based on a summary of the meeting and the action items from the meeting.

## Launching the solution

1. First
2. Next
3. Then


## Developing new features

### Set up local environment for Azure Function development

### Power Platform solution architecture 