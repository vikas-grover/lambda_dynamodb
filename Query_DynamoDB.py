import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

session = boto3.Session(profile_name = 'awslambda', region_name = 'us-east-1')
conn = session.client('dynamodb', region_name = 'us-east-1')
dyn_res = session.resource('dynamodb', region_name = 'us-east-1')

tablelist = conn.list_tables()
for table in tablelist['TableNames']:
	response = conn.describe_table(TableName=table)
	print(response)

for table in tablelist['TableNames']:	
	dbtable = dyn_res.Table(table)
	print(dbtable.creation_date_time)
	'''
	response = dbtable.scan(
		ScanFilter={
			"tweetText": {
						"AttributeValueList": ["Hillary"],
						"ComparisonOperator": "CONTAINS"
						}
					}
		)
	'''
	response = dbtable.scan(
		FilterExpression=Attr('tweetText').contains('Hillary')
		)
	print(response['Count'])
	with open('output.txt', mode="w", encoding="utf-8") as file:
		for item in response['Items']:
			#print(item)
			file.write(json.dumps(item,default = default)+'\n')
			#file.write(json.dumps([item for item in response['Items']],default = default))