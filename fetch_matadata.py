import boto3
import json
import os

def auth() -> object:
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
    role_arn = os.getenv("role_arn")

    sts_client = boto3.client(
        'sts',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=SECRET_ACCESS_KEY
    )

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='my-session'
    )

    credentials = response['Credentials']
    return credentials

def fetch_metadata(credentials: dict) -> dict:
    DATABASE = 'silver_db_test'
    tableName = 'appril'

    credentials = auth()

    glue = boto3.client(
        'glue',
        region_name="ca-central-1",
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    response = glue.get_table(
        DatabaseName=DATABASE,
        Name=tableName,
    )

    data = json.dumps(response, default=str)
    return {
        # "result": json.loads(data)
        "result": data
    }

def main():
    credentials = auth()
    return fetch_metadata(credentials)

if __name__ == "__main__":
    print(main())
