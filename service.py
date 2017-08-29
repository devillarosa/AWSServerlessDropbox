import sys
import boto3
import json
import re
import collections
import pymysql
import rds_config

rds_host = "devinmydb.cpvtwhh9r9mc.us-west-1.rds.amazonaws.com"
rds_port = 3306
db_user = rds_config.db_username
db_password = rds_config.db_password
db_name = rds_config.db_name

try:
    conn = pymysql.connect(rds_host, port=rds_port, user=db_user, passwd=db_password, db=db_name, connect_timeout=5)
except:
    sys.exit()


def handler(event, context):

    client = boto3.client('s3')
    bucket_name = 'devinvillarosa-sjsu-public'

    dict_response = client.list_objects(Bucket=bucket_name)

    # extract contents from the original dictionary
    content_list = dict_response['Contents']


    output_dict = {}
    for content in content_list:
        content_key = content['Key']
        url = client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': content_key})
        output_dict[content_key] = url

        # Sorts the Dictionary
        output_dict = collections.OrderedDict(sorted(output_dict.items()))

        # Transforms to JSON notation
        output = json.dumps(output_dict, ensure_ascii=False)
        resp = {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": output
                }

        return resp



