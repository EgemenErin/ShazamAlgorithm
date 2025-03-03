from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import base64
from database.database import FingerprintDatabase
from algorithm.matcher import identify_song

app = Flask(__name__)

# Initialize fingerprint database
db = FingerprintDatabase()
if os.path.exists('fingerprint_db.pkl'):
    db.load('fingerprint_db.pkl')
    print(f"Loaded database with {len(db.songs)} songs")

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/save-recording', methods=['POST'])
def save_recording():
    """Save an audio recording from the browser"""
    try:
        # Get audio data
        audio_data = request.json.get('audio')

        # Remove the "data:audio/wav;base64," part
        audio_data = audio_data.split(',')[1]

        # Generate a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"recording-{timestamp}.wav"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Decode and save the file
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(audio_data))

        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Recording saved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving recording: {str(e)}'
        })


@app.route('/identify', methods=['POST'])
def identify():
    """Identify a song from an audio recording"""
    try:
        # Get audio data
        audio_data = request.json.get('audio')

        # Remove the "data:audio/wav;base64," part
        audio_data = audio_data.split(',')[1]

        # Save to a temporary file
        temp_file = os.path.join(UPLOAD_FOLDER, 'temp.wav')
        with open(temp_file, "wb") as f:
            f.write(base64.b64decode(audio_data))

        # Identify the song
        result, confidence = identify_song(temp_file, db)

        return jsonify({
            'success': True,
            'result': result,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error identifying song: {str(e)}'
        })


@app.route('/add-to-db', methods=['POST'])
def add_to_db():
    """Add a recording to the fingerprint database"""
    try:
        filename = request.json.get('filename')
        song_name = request.json.get('songName')

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Rename the file with the song name
        new_filename = f"{song_name.replace(' ', '_')}.wav"
        new_filepath = os.path.join(UPLOAD_FOLDER, new_filename)

        # If it's not just a temp file, rename it
        if filename != 'temp.wav':
            os.rename(filepath, new_filepath)

        # Add to database
        song_id = db.add_song(new_filepath)

        # Save database
        db.save('fingerprint_db.pkl')

        return jsonify({
            'success': True,
            'songId': song_id,
            'message': f'Added "{song_name}" to the database'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error adding to database: {str(e)}'
        })


if __name__ == '__main__':
    app.run(debug=True)