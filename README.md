# dspam-trainer

Script to feed back false positives and negatives to DSpam

## Rationale
When running your own email server you have no control over which mail client the end user uses. Some mail clients have report as spam buttons, others don't. However the majority of them will not allow you to train the spam filter on the server. So we have to be creative.

## The solution
All email client are capable of moving emails between folders. So we setup a few special folders to help report spam and ham back to the spam filter on the server. 
We have a Quarantine folder which is where all the emails marked as spam are delivered to. In addition we have the now standard Junk folder but we also create one called 'Not Junk'.  
Ham is delivered to your Inbox and Spam goes to Quarantine.
### False negatives
I.e. spam that manages to sneak through into your inbox. The user moves the spam email into the Junk folder. Within a given time period the dspam-trainer script is executed. It will detect the new email in the Junk folder and perform the following

 - Extract the dspam-signature from the email headers
 - Call dspam and report the email as spam
 - Delete the email, permanently

### False positives
I.e. ham that got marked as spam. These will be found in the Quarantine folder and when the user spots a false positive they will move the email to 'Not Junk'. From there the dspam-trainer script will perform the following

- Extract the dspam-signature from the email headers
- Call dspam and report the email as innocent
- Move the email into the Inbox 
