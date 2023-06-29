import boto3
import io
import base64
from PIL import Image
import json

rekognition_client = boto3.client('rekognition')

def lambda_handler(event, context):
    # Get the base64 encoded image from the event
    body = json.loads(event['body'])
    base64_image = body['image']

    # Convert base64 image to binary format
    image_bytes = base64.b64decode(base64_image)

    # Call DetectFaces API
    response = rekognition_client.detect_faces(
        Image={
            'Bytes': image_bytes
        }
    )

    # Extract bounding box coordinates for first detected face
    face_details = response['FaceDetails'][0]
    bbox = face_details['BoundingBox']

    # Get image width and height
    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size

    # Convert bounding box coordinates to pixel values
    left = int(bbox['Left'] * width)
    top = int(bbox['Top'] * height)
    right = int((bbox['Left'] + bbox['Width']) * width)
    bottom = int((bbox['Top'] + bbox['Height']) * height)

    # Crop image to bounding box
    image = Image.open(io.BytesIO(image_bytes))
    cropped_image = image.crop((left, top, right, bottom))

    # Convert cropped image to base64 encoded string
    buffer = io.BytesIO()
    cropped_image.save(buffer, format='JPEG')
    cropped_image_str = base64.b64encode(buffer.getvalue()).decode()

    # Return the cropped image as a base64 encoded string
    return {'cropped_image': cropped_image_str}
