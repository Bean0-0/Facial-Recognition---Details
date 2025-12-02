const API_BASE_URL = '/api';

// Capture Instagram Livestream
async function captureLivestream() {
    const livestreamUrl = document.getElementById('livestreamUrl').value;
    const statusDiv = document.getElementById('livestreamStatus');
    
    if (!livestreamUrl) {
        showStatus(statusDiv, 'Please enter a livestream URL', 'error');
        return;
    }
    
    try {
        showStatus(statusDiv, 'Capturing livestream...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/livestream/capture`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ livestreamUrl })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus(statusDiv, `Success! Capture ID: ${data.captureId}. ${data.note}`, 'success');
        } else {
            showStatus(statusDiv, `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(statusDiv, `Error: ${error.message}`, 'error');
    }
}

// Upload and process video
async function uploadVideo() {
    const fileInput = document.getElementById('videoUpload');
    const statusDiv = document.getElementById('uploadStatus');
    
    if (!fileInput.files.length) {
        showStatus(statusDiv, 'Please select a video file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('video', fileInput.files[0]);
    
    try {
        showStatus(statusDiv, 'Processing video...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/facial-recognition/process`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus(statusDiv, `Success! Process ID: ${data.processId}. ${data.message}`, 'success');
            
            // Simulate showing detected faces (in production, this would be real data)
            displayMockFaces();
        } else {
            showStatus(statusDiv, `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(statusDiv, `Error: ${error.message}`, 'error');
    }
}

// Display mock faces for demonstration
function displayMockFaces() {
    const facesContainer = document.getElementById('facesContainer');
    
    const mockFaces = [
        {
            faceId: 'face-001',
            confidence: 0.95,
            personName: 'John Doe',
            attributes: {
                age: 25,
                emotion: 'happy'
            }
        },
        {
            faceId: 'face-002',
            confidence: 0.89,
            personName: 'Jane Smith',
            attributes: {
                age: 30,
                emotion: 'neutral'
            }
        }
    ];
    
    facesContainer.innerHTML = '';
    
    mockFaces.forEach(face => {
        const faceCard = document.createElement('div');
        faceCard.className = 'face-card';
        faceCard.innerHTML = `
            <h3>${face.personName || 'Unknown'}</h3>
            <p><strong>Face ID:</strong> ${face.faceId}</p>
            <p><strong>Confidence:</strong> ${(face.confidence * 100).toFixed(1)}%</p>
            <p><strong>Age:</strong> ~${face.attributes.age}</p>
            <p><strong>Emotion:</strong> ${face.attributes.emotion}</p>
            <button onclick="searchPersonDetails('${face.faceId}')">View Details</button>
        `;
        facesContainer.appendChild(faceCard);
    });
}

// Search for person details by faceId
async function searchPersonDetails(faceId) {
    try {
        const response = await fetch(`${API_BASE_URL}/person-details/search?faceId=${faceId}`);
        const data = await response.json();
        
        if (response.ok) {
            displayPersonDetails(data.person);
        } else {
            alert(`Person not found: ${data.message}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Load all persons from database
async function loadPersonDatabase() {
    const personDatabase = document.getElementById('personDatabase');
    
    try {
        const response = await fetch(`${API_BASE_URL}/person-details`);
        const data = await response.json();
        
        if (response.ok) {
            personDatabase.innerHTML = '';
            
            if (data.persons.length === 0) {
                personDatabase.innerHTML = '<p class="placeholder-text">No persons in database</p>';
                return;
            }
            
            data.persons.forEach(person => {
                const personCard = createPersonCard(person);
                personDatabase.appendChild(personCard);
            });
        } else {
            personDatabase.innerHTML = `<p class="placeholder-text error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        personDatabase.innerHTML = `<p class="placeholder-text error">Error: ${error.message}</p>`;
    }
}

// Create person card element
function createPersonCard(person) {
    const personCard = document.createElement('div');
    personCard.className = 'person-card';
    
    const interestsHtml = person.interests && person.interests.length > 0
        ? `<div class="interests-tags">
            ${person.interests.map(interest => `<span class="interest-tag">${interest}</span>`).join('')}
           </div>`
        : '<span style="color: #999;">No interests listed</span>';
    
    personCard.innerHTML = `
        <h3>${person.name}</h3>
        <div class="info-row">
            <span class="info-label">Face ID:</span>
            <span class="info-value">${person.faceId}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Birthday:</span>
            <span class="info-value">${person.birthday || 'Not specified'}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Occupation:</span>
            <span class="info-value">${person.occupation || 'Not specified'}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Location:</span>
            <span class="info-value">${person.location || 'Not specified'}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Interests:</span>
            <span class="info-value">${interestsHtml}</span>
        </div>
        ${person.socialMedia && (person.socialMedia.instagram || person.socialMedia.twitter) 
            ? `<div class="info-row">
                <span class="info-label">Social Media:</span>
                <span class="info-value">
                    ${person.socialMedia.instagram || ''} 
                    ${person.socialMedia.twitter || ''}
                </span>
               </div>`
            : ''}
    `;
    
    return personCard;
}

// Display person details in a modal or section
function displayPersonDetails(person) {
    const personDatabase = document.getElementById('personDatabase');
    personDatabase.innerHTML = '';
    const personCard = createPersonCard(person);
    personDatabase.appendChild(personCard);
    
    // Scroll to the person database section
    personDatabase.scrollIntoView({ behavior: 'smooth' });
}

// Add new person to database
async function addPerson(event) {
    event.preventDefault();
    
    const statusDiv = document.getElementById('addPersonStatus');
    
    const personData = {
        name: document.getElementById('personName').value,
        birthday: document.getElementById('personBirthday').value,
        faceId: document.getElementById('personFaceId').value,
        occupation: document.getElementById('personOccupation').value,
        location: document.getElementById('personLocation').value,
        interests: document.getElementById('personInterests').value
            .split(',')
            .map(i => i.trim())
            .filter(i => i.length > 0)
    };
    
    try {
        showStatus(statusDiv, 'Adding person...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/person-details`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(personData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus(statusDiv, `Success! ${data.person.name} has been added to the database.`, 'success');
            document.getElementById('addPersonForm').reset();
            
            // Reload the person database
            setTimeout(() => {
                loadPersonDatabase();
            }, 1000);
        } else {
            showStatus(statusDiv, `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(statusDiv, `Error: ${error.message}`, 'error');
    }
}

// Utility function to show status messages
function showStatus(element, message, type) {
    element.textContent = message;
    element.className = `status-message ${type}`;
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    console.log('Facial Recognition System Initialized');
    
    // Check API health
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('API Status:', data);
        })
        .catch(error => {
            console.error('API connection error:', error);
        });
});
