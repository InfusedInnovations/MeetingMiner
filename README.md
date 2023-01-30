# MeetingMiner

<img src="/MM-logo.png" width="200px" height="200px" style="border-radius:50%" />

A GPT-based natural language cognitive assistant for extracting valuable information from Microsoft Teams meetings.
MeetingMiner can write follow-up emails to operationalize information, identifying action items to be shared with teammates, and more.

This repository is a work in progress, and will be available for use within the next few days. Interested in launching the MeetingMiner solution? Contact brennan@infusedinnovations.com!

## Solution demonstration

A demonstration of the MeetingMiner solution can be found <a href="https://www.figma.com/proto/B6nuI0whiPscjNVECBvpwr/MeetingMiner-Demo?node-id=180%3A298&scaling=scale-down&page-id=55%3A0&starting-point-node-id=180%3A298" target="_blank">here</a>.

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
2. Azure Function App code.
    * Hosts the OpenAI code for the A.I. to process meeting transcript data into more valuable outputs.
    * Contains a function which can be called to write a follow-up email based on a summary of the meeting and the action items from the meeting.

3. Azure infrastructure resources.
    * Azure AD application which requests the necessary permissions.
    * Security group to allocate application permissions and licensing to the application users on the tenant.

## Launching the solution

1. <a href="https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/add-application-portal">Create an enterprise application</a> in Azure. The following Microsoft Graph permissions must be granted.
    * User.Read
    * OnlineMeetings.Read.All
    * OnlineMeetings.ReadWrite.All
    * OnlineMeetingArtifact.Read.All
    * Calendars.Read
    * CallRecords.Read.All
    * OnlineMeetingTranscript.Read.All
    * Calendars.ReadWrite
2. <a href="https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal">Create an Azure OpenAI resource</a> and deploy a GPT-3 model instance.
3. Download the code in the repository and use it to deploy the Azure functions to your Azure tenant. Fill in the following application settings under your Azure Function App > Configuration in the Azure Portal.
    * AZURE_OAI_API_KEY. The API key for the Azure OpenAI resource you just created.
    * AZURE_OAI_MODEL_DEPLOYMENT. The name of the GPT-3 model you just deployed.
    * PRODUCTION. Use the value of "1" in the Azure Portal (and "0" locally if you want some added development benefits.
4. Import the Power Platform solution (user interface, AI processing logic, reminders/notifications).
    * Fill in the following environment variables.
      - lead_mm_developer_email. The lead developer who wants to be notified about application usage and performance.
      - optedInUsers. A list of email addresses for the users in your tenant that want to use your application. Format should be, i.e., {"optedIn":["user1@mytenant.com", "user2@mytenant.com"]}.
      - production. Use the value "Yes" when your application is in production or "No" when you want to take different actions in your flows while under development.
      - production_application_id. The ID of the enterprise application you set up in the step above.
      - production_client_secret. The client secret of the enterprise application you set up in the step above.
      - production_tenant_id. The ID of your azure tenant. Can be found in the Azure Portal.
    * Create connections when prompted.
    
 Congratulations! You're ready to start using MeetingMiner to increase your team's productivity.


<!-- ## Developing new features ### Set up local environment for Azure Function development ### Power Platform solution architecture -->




 
