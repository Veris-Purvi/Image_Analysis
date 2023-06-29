import json
import boto3
from io import BytesIO
from PIL import Image
from PIL import _imaging
import base64

def lambda_handler(event, context):
    
    # Get the image from the API Gateway request body
    try:
        print(event)
        body = json.loads(event['body'])
        image_b64 = body['image']
        
        # Decode the base64-encoded image
        image_data = BytesIO(base64.b64decode(image_b64))
        image = Image.open(image_data)
        
        # Create a bytes-like object from the image
        stream = BytesIO()
        image.save(stream, format="JPEG")
        image_bytes = stream.getvalue()
        
        # Create a Rekognition client
        rekognition = boto3.client('rekognition')
        
        # Detect faces in the image
        response = rekognition.detect_protective_equipment(
            Image={
                'Bytes': image_bytes,
            },
            SummarizationAttributes={
                'MinConfidence': 80,
                'RequiredEquipmentTypes': ['FACE_COVER'],
            }
        )
        
        # Check if there are any people in the image wearing a face cover
        if 'Persons' in response and len(response['Persons']) > 0:
            for person in response['Persons']:
                if 'BodyParts' in person and len(person['BodyParts']) > 0:
                    for body_part in person['BodyParts']:
                        if 'EquipmentDetections' in body_part and len(body_part['EquipmentDetections']) > 0:
                            for equipment_detection in body_part['EquipmentDetections']:
                                if equipment_detection['Type'] == 'FACE_COVER':
                                    return {
                                        'statusCode': 200,
                                        'body': json.dumps({'message': 'Face Mask detected'})
                                    }
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'No face mask detected'})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }
        