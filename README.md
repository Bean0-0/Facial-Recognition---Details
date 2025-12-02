# Facial Recognition System

A comprehensive web application with backend that captures video from Instagram livestreams, runs facial recognition, and retrieves detailed information about detected persons including name, birthday, interests, and more.

## Features

- 📹 **Instagram Livestream Capture**: Capture video from Instagram livestreams
- 🎥 **Video Upload & Processing**: Upload videos for facial recognition analysis
- 👤 **Facial Recognition**: Detect and identify faces in videos
- 📊 **Person Details Database**: Store and retrieve detailed information about people
- 🌐 **Web Interface**: User-friendly web interface for all operations
- 🔌 **RESTful API**: Complete REST API for programmatic access

## Technology Stack

- **Backend**: Node.js, Express.js
- **Frontend**: HTML5, CSS3, JavaScript
- **File Upload**: Multer
- **HTTP Client**: Axios
- **Environment Variables**: dotenv

## Project Structure

```
Facial-Recognition---Details/
├── server/
│   ├── index.js              # Main server file
│   └── routes/
│       ├── livestream.js     # Instagram livestream endpoints
│       ├── facialRecognition.js  # Facial recognition endpoints
│       └── personDetails.js  # Person database endpoints
├── public/
│   ├── index.html           # Frontend web interface
│   ├── styles.css           # Styling
│   └── script.js            # Frontend JavaScript
├── uploads/                 # Video upload directory (created automatically)
├── .env.example            # Environment variables template
├── .gitignore
├── package.json
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bean0-0/Facial-Recognition---Details.git
cd Facial-Recognition---Details
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:
- Instagram API credentials (if using official API)
- Facial recognition API credentials (AWS Rekognition, Azure Face API, etc.)
- Database credentials (if using external database)

4. Start the server:
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

5. Open your browser and navigate to:
```
http://localhost:3000
```

## API Endpoints

### Health Check
- **GET** `/api/health` - Check API status

### Instagram Livestream
- **POST** `/api/livestream/capture` - Capture Instagram livestream
  - Body: `{ "livestreamUrl": "https://..." }`
- **GET** `/api/livestream/status/:captureId` - Get capture status

### Facial Recognition
- **POST** `/api/facial-recognition/process` - Upload and process video
  - Form data with video file
- **POST** `/api/facial-recognition/analyze-frame` - Analyze single frame
  - Body: `{ "imageData": "base64..." }`
- **GET** `/api/facial-recognition/results/:processId` - Get processing results

### Person Details
- **GET** `/api/person-details` - Get all persons in database
- **GET** `/api/person-details/:personId` - Get person by ID
- **GET** `/api/person-details/search?faceId=xxx` - Search person by face ID
- **POST** `/api/person-details` - Add new person to database
  - Body: `{ "name": "...", "birthday": "...", "faceId": "...", "interests": [...], ... }`

## Usage

### 1. Capturing Instagram Livestream

Navigate to the web interface and enter an Instagram livestream URL in the "Instagram Livestream Capture" section. Click "Capture Livestream" to initiate the capture process.

**Note**: Instagram's official API has limited livestream access. You may need to:
- Use Instagram's official Business/Creator API
- Implement third-party streaming capture services
- Configure proper authentication credentials

### 2. Uploading Video for Analysis

In the "Upload Video for Analysis" section:
1. Select a video file (MP4, AVI, MOV, WEBM)
2. Click "Process Video"
3. The system will upload and analyze the video for faces

### 3. Viewing Detected Faces

After processing, detected faces will appear in the "Detected Faces" section with:
- Face ID
- Confidence score
- Detected attributes (age, emotion)
- Link to view full person details

### 4. Managing Person Database

**View all persons**: Click "Load All Persons" in the Person Database section

**Add new person**: Fill out the form in the "Add New Person" section with:
- Name (required)
- Face ID (required)
- Birthday
- Occupation
- Location
- Interests (comma-separated)

## Integration Guide

### Facial Recognition APIs

To enable actual facial recognition, integrate with one of these services:

#### AWS Rekognition
```javascript
const AWS = require('aws-sdk');
const rekognition = new AWS.Rekognition({ region: 'us-east-1' });

// Detect faces
const params = {
  Image: {
    Bytes: imageBuffer
  },
  Attributes: ['ALL']
};

rekognition.detectFaces(params, (err, data) => {
  // Process face detection results
});
```

#### Azure Face API
```javascript
const axios = require('axios');

const response = await axios.post(
  `${process.env.FACE_RECOGNITION_API_URL}/detect`,
  imageData,
  {
    headers: {
      'Ocp-Apim-Subscription-Key': process.env.FACE_RECOGNITION_API_KEY,
      'Content-Type': 'application/octet-stream'
    }
  }
);
```

### Instagram API Integration

For Instagram livestream access:

1. Register your app at [Facebook Developers](https://developers.facebook.com/)
2. Get Instagram Business/Creator API access
3. Implement OAuth 2.0 authentication
4. Use Instagram Graph API to access livestream data

## Database Integration

The current implementation uses in-memory storage. For production:

### PostgreSQL Example
```javascript
const { Pool } = require('pg');
const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
});

// Create persons table
CREATE TABLE persons (
  id SERIAL PRIMARY KEY,
  face_id VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  birthday DATE,
  interests TEXT[],
  occupation VARCHAR(255),
  location VARCHAR(255),
  social_media JSONB
);
```

## Security Considerations

⚠️ **Important Security Notes**:

1. **API Keys**: Never commit API keys to version control. Use `.env` file
2. **Authentication**: Implement user authentication before deploying to production
3. **Rate Limiting**: Add rate limiting to prevent API abuse
4. **Input Validation**: Validate all user inputs
5. **HTTPS**: Use HTTPS in production
6. **Privacy**: Ensure compliance with privacy laws (GDPR, CCPA) when storing personal data
7. **Consent**: Obtain proper consent before collecting facial recognition data

## Development

```bash
# Install dependencies
npm install

# Start development server with auto-reload
npm run dev

# Start production server
npm start
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Disclaimer

This application is for educational and research purposes. Ensure you have proper authorization and consent before using facial recognition on any individuals. Comply with all applicable laws and regulations regarding privacy and data protection.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Future Enhancements

- [ ] Real-time video stream processing
- [ ] Multiple face tracking in videos
- [ ] Face matching against larger databases
- [ ] Advanced analytics and reporting
- [ ] Mobile application
- [ ] WebSocket for real-time updates
- [ ] User authentication and authorization
- [ ] Cloud storage integration
- [ ] Advanced filtering and search
- [ ] Export data functionality