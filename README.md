# Image_Analysis

# Image Processing Lambda Functions

This repository contains two Lambda functions written in Python for image processing tasks using Amazon Rekognition service.



## Installation

1. Clone the repository

2. Install the required dependencies using pip:

   ```shell
   pip install -r requirements.txt
   ```

## Lambda Functions

### 1. Mask Detection

The `mask_detection.py` Lambda function detects if a person is wearing a face mask in an image.

#### Usage

To use the Mask Detection Lambda function, you can trigger it through API Gateway or invoke it directly. The Lambda function expects a base64-encoded image in the request body. It will analyze the image using Amazon Rekognition and determine if any person is wearing a face mask.

Example API request:

```http
POST /mask-detection
Content-Type: application/json

{
  "image": "<base64-encoded-image>"
}
```

Example API response:

```json
{
  "statusCode": 200,
  "body": {
    "message": "Face Mask detected"
  }
}
```

#### Error Handling

If there are any errors during the execution of the Lambda function, an appropriate error message will be returned in the response body with a status code of 400.

### 2. Image Cropping

The `crop_image.py` Lambda function crops an image based on the detected face using Amazon Rekognition service.

#### Usage

To use the Image Cropping Lambda function, you can trigger it through API Gateway or invoke it directly. The Lambda function expects a base64-encoded image in the request body. It will detect the face in the image using Amazon Rekognition, crop the image to the bounding box of the face, and return the cropped image as a base64-encoded string.

Example API request:

```http
POST /crop-image
Content-Type: application/json

{
  "image": "<base64-encoded-image>"
}
```

Example API response:

```json
{
  "statusCode": 200,
  "body": {
    "cropped_image": "<base64-encoded-cropped-image>"
  }
}
```



