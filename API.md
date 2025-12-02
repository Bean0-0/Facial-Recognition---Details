# API Documentation

## Base URL
```
http://localhost:3000/api
```

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Facial Recognition API is running",
  "timestamp": "2025-12-02T01:00:00.000Z"
}
```

---

## Instagram Livestream Endpoints

### POST /livestream/capture
Capture video from an Instagram livestream.

**Request Body:**
```json
{
  "livestreamUrl": "https://www.instagram.com/live/..."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Livestream capture initiated",
  "livestreamUrl": "https://www.instagram.com/live/...",
  "captureId": "1234567890",
  "note": "Configure Instagram API credentials in .env file for actual implementation"
}
```

### GET /livestream/status/:captureId
Get the status of a livestream capture.

**Parameters:**
- `captureId` - The ID returned from the capture endpoint

**Response:**
```json
{
  "captureId": "1234567890",
  "status": "processing",
  "framesProcessed": 0,
  "timestamp": "2025-12-02T01:00:00.000Z"
}
```

---

## Facial Recognition Endpoints

### POST /facial-recognition/process
Upload and process a video file for facial recognition.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: Form data with video file under key 'video'

**Response:**
```json
{
  "processId": "1234567890",
  "videoFile": "1234567890.mp4",
  "status": "processing",
  "detectedFaces": [],
  "message": "Video uploaded successfully. Configure facial recognition API in .env for actual processing."
}
```

### POST /facial-recognition/analyze-frame
Analyze a single frame for faces.

**Request Body:**
```json
{
  "imageData": "base64_encoded_image_data"
}
```

**Response:**
```json
{
  "status": "success",
  "facesDetected": 1,
  "faces": [
    {
      "faceId": "face-1",
      "confidence": 0.95,
      "boundingBox": {
        "x": 100,
        "y": 100,
        "width": 200,
        "height": 200
      },
      "attributes": {
        "age": 25,
        "gender": "unknown",
        "emotion": "neutral"
      }
    }
  ],
  "timestamp": "2025-12-02T01:00:00.000Z"
}
```

### GET /facial-recognition/results/:processId
Get processing results for a video.

**Parameters:**
- `processId` - The ID returned from the process endpoint

**Response:**
```json
{
  "processId": "1234567890",
  "status": "completed",
  "detectedFaces": [],
  "timestamp": "2025-12-02T01:00:00.000Z"
}
```

---

## Person Details Endpoints

### GET /person-details
Get all persons in the database.

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "persons": [
    {
      "id": "1",
      "faceId": "face-001",
      "name": "John Doe",
      "birthday": "1990-05-15",
      "interests": ["technology", "music", "sports"],
      "occupation": "Software Engineer",
      "location": "New York, USA",
      "socialMedia": {
        "instagram": "@johndoe",
        "twitter": "@johndoe"
      }
    }
  ]
}
```

### GET /person-details/:personId
Get detailed information about a specific person.

**Parameters:**
- `personId` - The ID of the person

**Response:**
```json
{
  "status": "success",
  "person": {
    "id": "1",
    "faceId": "face-001",
    "name": "John Doe",
    "birthday": "1990-05-15",
    "interests": ["technology", "music", "sports"],
    "occupation": "Software Engineer",
    "location": "New York, USA",
    "socialMedia": {
      "instagram": "@johndoe",
      "twitter": "@johndoe"
    }
  }
}
```

### GET /person-details/search
Search for a person by face ID.

**Query Parameters:**
- `faceId` - The face ID to search for

**Example:**
```
GET /api/person-details/search?faceId=face-001
```

**Response:**
```json
{
  "status": "success",
  "person": {
    "id": "1",
    "faceId": "face-001",
    "name": "John Doe",
    "birthday": "1990-05-15",
    "interests": ["technology", "music", "sports"],
    "occupation": "Software Engineer",
    "location": "New York, USA",
    "socialMedia": {
      "instagram": "@johndoe",
      "twitter": "@johndoe"
    }
  }
}
```

### POST /person-details
Add a new person to the database.

**Request Body:**
```json
{
  "name": "Alice Johnson",
  "faceId": "face-003",
  "birthday": "1992-08-10",
  "interests": ["reading", "yoga"],
  "occupation": "Teacher",
  "location": "Chicago, USA",
  "socialMedia": {
    "instagram": "@alicejohnson"
  }
}
```

**Required Fields:**
- `name` - Person's name
- `faceId` - Unique face identifier

**Optional Fields:**
- `birthday` - Date of birth (YYYY-MM-DD format)
- `interests` - Array of interests
- `occupation` - Job title or occupation
- `location` - Location information
- `socialMedia` - Object containing social media handles

**Response:**
```json
{
  "status": "success",
  "message": "Person added successfully",
  "person": {
    "id": "3",
    "faceId": "face-003",
    "name": "Alice Johnson",
    "birthday": "1992-08-10",
    "interests": ["reading", "yoga"],
    "occupation": "Teacher",
    "location": "Chicago, USA",
    "socialMedia": {
      "instagram": "@alicejohnson"
    }
  }
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common HTTP Status Codes

- `200` - Success
- `201` - Created (for POST requests)
- `400` - Bad Request (missing or invalid parameters)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

---

## Examples Using cURL

### Capture Instagram Livestream
```bash
curl -X POST http://localhost:3000/api/livestream/capture \
  -H "Content-Type: application/json" \
  -d '{"livestreamUrl": "https://www.instagram.com/live/abc123"}'
```

### Upload Video for Processing
```bash
curl -X POST http://localhost:3000/api/facial-recognition/process \
  -F "video=@/path/to/video.mp4"
```

### Add New Person
```bash
curl -X POST http://localhost:3000/api/person-details \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "faceId": "face-003",
    "birthday": "1992-08-10",
    "interests": ["reading", "yoga"],
    "occupation": "Teacher"
  }'
```

### Search Person by Face ID
```bash
curl http://localhost:3000/api/person-details/search?faceId=face-001
```

### Get All Persons
```bash
curl http://localhost:3000/api/person-details
```
