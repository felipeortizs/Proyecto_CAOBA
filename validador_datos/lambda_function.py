import json
from reader_validator import ReaderValidator

def handler(event, context):
    try:
        data_type = event.get('type', None)
        s3_file_path = event.get('s3_file_path', None)
        
        if data_type is None or s3_file_path is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Both 'type' and 's3_file_path' are required."})
            }

        try:
            rv = ReaderValidator(data_type, s3_file_path)
        except Exception as err:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": err})
            }

        result = rv.validate()

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
