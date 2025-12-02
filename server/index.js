const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs').promises;
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Ensure upload directory exists
async function ensureUploadDir() {
  try {
    await fs.mkdir('uploads', { recursive: true });
    console.log('Upload directory ready');
  } catch (error) {
    console.error('Failed to create upload directory:', error);
  }
}

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Import routes
const livestreamRoutes = require('./routes/livestream');
const facialRecognitionRoutes = require('./routes/facialRecognition');
const personDetailsRoutes = require('./routes/personDetails');

// Routes
app.use('/api/livestream', livestreamRoutes);
app.use('/api/facial-recognition', facialRecognitionRoutes);
app.use('/api/person-details', personDetailsRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'Facial Recognition API is running',
    timestamp: new Date().toISOString()
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: err.message 
  });
});

// Start server
async function startServer() {
  await ensureUploadDir();
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} to access the application`);
  });
}

startServer();

module.exports = app;
