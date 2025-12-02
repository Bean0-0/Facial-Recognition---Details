const express = require('express');
const router = express.Router();

// In-memory database for demo purposes
// In production, use a real database like PostgreSQL, MongoDB, etc.
const personDatabase = [
  {
    id: '1',
    faceId: 'face-001',
    name: 'John Doe',
    birthday: '1990-05-15',
    interests: ['technology', 'music', 'sports'],
    occupation: 'Software Engineer',
    location: 'New York, USA',
    socialMedia: {
      instagram: '@johndoe',
      twitter: '@johndoe'
    }
  },
  {
    id: '2',
    faceId: 'face-002',
    name: 'Jane Smith',
    birthday: '1988-09-22',
    interests: ['art', 'travel', 'photography'],
    occupation: 'Photographer',
    location: 'Los Angeles, USA',
    socialMedia: {
      instagram: '@janesmith',
      twitter: '@janesmith'
    }
  }
];

/**
 * GET /api/person-details/search
 * Search for person by faceId
 * Query params: faceId
 */
router.get('/search', async (req, res) => {
  try {
    const { faceId } = req.query;
    
    if (!faceId) {
      return res.status(400).json({ error: 'faceId is required' });
    }

    const person = personDatabase.find(p => p.faceId === faceId);
    
    if (!person) {
      return res.status(404).json({ 
        error: 'Person not found',
        message: 'No matching person found for the given faceId'
      });
    }

    res.json({
      status: 'success',
      person: person
    });
    
  } catch (error) {
    console.error('Error searching for person:', error);
    res.status(500).json({ 
      error: 'Failed to search for person',
      message: error.message 
    });
  }
});

/**
 * GET /api/person-details/:personId
 * Get detailed information about a person by ID
 */
router.get('/:personId', async (req, res) => {
  try {
    const { personId } = req.params;
    
    const person = personDatabase.find(p => p.id === personId);
    
    if (!person) {
      return res.status(404).json({ 
        error: 'Person not found',
        message: 'No person found with the given ID'
      });
    }

    res.json({
      status: 'success',
      person: person
    });
    
  } catch (error) {
    console.error('Error getting person details:', error);
    res.status(500).json({ 
      error: 'Failed to get person details',
      message: error.message 
    });
  }
});

/**
 * POST /api/person-details
 * Add a new person to the database
 * Body: { name, birthday, interests, occupation, location, faceId, socialMedia }
 */
router.post('/', async (req, res) => {
  try {
    const { name, birthday, interests, occupation, location, faceId, socialMedia } = req.body;
    
    if (!name || !faceId) {
      return res.status(400).json({ 
        error: 'Name and faceId are required' 
      });
    }

    const newPerson = {
      id: (personDatabase.length + 1).toString(),
      faceId: faceId,
      name: name,
      birthday: birthday || null,
      interests: interests || [],
      occupation: occupation || null,
      location: location || null,
      socialMedia: socialMedia || {}
    };

    personDatabase.push(newPerson);

    res.status(201).json({
      status: 'success',
      message: 'Person added successfully',
      person: newPerson
    });
    
  } catch (error) {
    console.error('Error adding person:', error);
    res.status(500).json({ 
      error: 'Failed to add person',
      message: error.message 
    });
  }
});

/**
 * GET /api/person-details
 * Get all persons in database
 */
router.get('/', async (req, res) => {
  try {
    res.json({
      status: 'success',
      count: personDatabase.length,
      persons: personDatabase
    });
    
  } catch (error) {
    console.error('Error getting all persons:', error);
    res.status(500).json({ 
      error: 'Failed to get persons',
      message: error.message 
    });
  }
});

module.exports = router;
