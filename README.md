# MeetingMiner

<img src="/MM-logo.png" width="200px" height="200px" style="border-radius:50%" />

A GPT-based natural language cognitive assistant for extracting valuable information from Microsoft Teams meetings.
MeetingMiner can write follow-up emails to operationalize information, identifying action items to be shared with teammates, and more.

Facing difficulties? <a href="https://www.infusedinnovations.com/lets-collaborate">Contact us</a>! We are very responsive and open to helping you launch MeetingMiner at your organization.

## Pre-requisites

* Experience developing solutions with Power Platform including: Power Automate, Power Apps, and Dataverse.
* Experience developing Azure solutions including Azure Functions and minimal experience with Azure AD for delegating MS Graph application permissions.
* A global admin account
* <a href="https://learn.microsoft.com/en-us/power-platform/admin/pricing-billing-skus">Power Platform administration/licensing knowledge</a>. Licenses will need to be administered for Power Apps for your users to leverage the solution.

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
2. <a href="https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal" target="_blank">Create an Azure OpenAI resource</a> and deploy a GPT-3 model instance.
3. Download the code in the repository and use it to deploy the Azure functions to your Azure tenant. Fill in the following application settings under your Azure Function App > Configuration in the Azure Portal.
    * AZURE_OAI_API_KEY. The API key for the Azure OpenAI resource you just created.
    * AZURE_OAI_MODEL_DEPLOYMENT. The name of the GPT-3 model you just deployed.
    * PRODUCTION. Use the value of 1 in the Azure Portal (and 0 locally for development).
4. <a href="https://learn.microsoft.com/en-us/power-apps/maker/data-platform/import-update-export-solutions" target="_blank">Import the Power Platform solution</a> (user interface, AI processing logic, reminders/notifications).
    * Fill in the following <a href="https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables" target="_blank">environment variables</a>.
      - <b>lead_mm_developer_email</b>. The lead developer who wants to be notified about application usage and performance.
      - <b>optedInUsers</b>. A list of email addresses for the users in your tenant that want to use your application. Format should be, i.e., {"optedIn":["user1@mytenant.com", "user2@mytenant.com"]}.
      - <b>production</b>. Use the value "Yes" when your application is in production or "No" when you want to take different actions in your flows while under development.
      - <b>production_application_id</b>. The ID of the enterprise application you set up in the step above.
      - <b>production_client_secret</b>. The <a href="https://learn.microsoft.com/en-us/answers/questions/834401/hi-i-want-my-client-id-and-client-secret-key" target="_blank">client secret</a> of the enterprise application you set up in the step above.
      - <b>production_tenant_id</b>. The ID of your Azure tenant. Can be found in the <a href="portal.azure.com" target="_blank">Azure Portal</a> by searching "tenant properties".
      - <b>callRecordsNotificationURL</b>. The URL available in the trigger of the "MeetingMiner Request-triggered flow - Mine Meeting" trigger.
      - <b>meetingStartURL</b>. The URL available in the trigger of the "MeetingMiner Send Reminder When Meeting Starts" trigger.
      - <b>azureFnURLMMHTTP</b>. The URL of the main Azure Function you launched above.
      - <b>azureFnURLWriteFollowUp</b>. The URL of the Azure Function for writing the follow-up email, which you launched above.
    * Create data connections when prompted.
    
 Congratulations! You're ready to start using MeetingMiner to increase your team's productivity.

## Disclaimers

* Infused Innovations is not financially liable for the operating costs incurred while using this solution.
* This solution is not for re-sale.

<!-- ## Developing new features ### Set up local environment for Azure Function development ### Power Platform solution architecture -->




 
