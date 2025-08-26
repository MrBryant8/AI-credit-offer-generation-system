from django.db import models

class AgentConfig(models.Model):
    id = models.AutoField(primary_key=True)
    email_task_description = models.TextField(null=True)
    default_task_description = models.TextField(default="""Draft a professional and compliant credit approval email using the provided client, offer,
    and company context. The email must clearly present the approved offer details, next steps,
    and any required documents, while maintaining a courteous, trustworthy tone appropriate
    for a regulated financial institution. At the end the recepient should be prompted to view the offer details via {more_details_link}. 
    The client name is {client_name}. The client is requesting the loan of {loan_amount} in euros, that he pledges to pay for approximately {loan_duration} in months.
    When describing the loan, adhere to the generic loan description, provided by the credit bank - {loan_type_description}. 
    Also please keep in mind the demographic details of the person sucha as age - {client_age}, sex - {client_sex}.
    Do not explicitly mention them, just adjust your tone based on the client's demographic situation, so that the email sounds more appealing to the client.
    As next steps, make sure to prompt the user to accept the offer, if they like it, and book a consulting hour with a specialist at {bank_address} through {bank_phone_number}.
    Make sure to end the email with a formal regard from SmartCredit. You can use emojis if the demographic situation of the customer finds it suitable.""")