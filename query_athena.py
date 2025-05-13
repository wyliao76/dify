import boto3
import json
import time
import csv
from io import StringIO
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


def query_athena(query: str, credentials: object) -> object:
    OUTPUT_LOCATION = 's3://aws-athena-query-results-ca-central-1-264057463295'
    DATABASE = 'silver_db_test'

    athena = boto3.client(
            'athena',
            region_name="ca-central-1",
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )

    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': OUTPUT_LOCATION
        }
    )

    # print(response)

    query_execution_id = response['QueryExecutionId']
    max_execution = 100
    state = 'QUEUED'
    while (max_execution > 0 and state in ['RUNNING', 'QUEUED']):
        max_execution = max_execution - 1
        response = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = response['QueryExecution']['Status']['State']
        # print(state)
        time.sleep(1)
        if state == 'FAILED':
            print(response['QueryExecution'])
            raise ConnectionError('Query failed!')
        if state == 'SUCCEEDED':
            # print(response['QueryExecution'])
            s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']

    s3 = boto3.client(
        's3',
        region_name="ca-central-1",
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    results = s3_path.split("/")
    bucket = results[2]
    key = results[3]

    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read().decode('utf-8')
    # # print(body)

    f = StringIO(body)
    reader = csv.DictReader(f)

    response = list(reader)
    data = json.dumps(response, indent=4)
    return {
        "result": json.loads(data)
    }

def main():
    credentials = auth()

    query = '''SELECT DISTINCT(company_name)
        FROM appril
        WHERE status_group = 'Active' 
        AND pest_cat LIKE '%Insecticide%' 
        AND LOWER(ai_names) LIKE '%neem%'
        ORDER BY company_name DESC
        '''

    # query = "SELECT DISTINCT company_name\nFROM appril\nWHERE pest_cat = 'Insecticide'\nAND ais LIKE '%Neem%';"

    # query = '''
    # SELECT product_name, reg_num, company_name, pest_cat 
    # FROM appril 
    # WHERE first_reg_dt>= date_add('day', -30, current_timestamp)
    # '''

    return query_athena(query, credentials)


if __name__ == "__main__":
    print(main())
