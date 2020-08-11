import json
from scraper.models import Session, Job


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def testPg(event, context):
    session = Session()
    ids = [j.job_id for j in session.query(Job.job_id).filter_by(site="baunetz").order_by(Job.job_id)]
    print(ids)
    # session.close()
    print("Got existing IDS in DB, to avoid saving duplicates... [" + str(len(ids)) + "]")
    # return ids
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(ids)
    }

    return response
