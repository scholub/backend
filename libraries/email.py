from os import getenv

from boto3 import client # pyright: ignore[reportMissingTypeStubs, reportUnknownVariableType]

email = client( # pyright: ignore[reportUnknownVariableType]
  "ses",
  aws_access_key_id = getenv("AWS_SERVER_PUBLIC_KEY", ""),
  aws_secret_access_key = getenv("AWS_SERVER_SECRET_KEY", ""),
  region_name = getenv("AWS_SERVER_REGION", "eu-west-2")
)

def send_email(title: str, body: str, receiver: list[str]):
  for i in receiver:
    email.send_email( # pyright: ignore[reportUnknownMemberType]
      Destination={
        'ToAddresses': [i]
      },
      Message = {
        'Body': {
          'Html': {'Charset': 'UTF-8', 'Data': body}
        },
        'Subject': {'Charset': 'UTF-8', 'Data': title}
      },
      Source = getenv("EMAIL_SENDER", "Scholub <scholub@schale.misile.xyz>")
    )

