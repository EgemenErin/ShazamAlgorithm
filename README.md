# Audio Recorder & Shazam Clone

This project is an audio fingerprinting application inspired by Shazam. It allows users to record audio, visualize the waveform in real time, and identify songs by matching audio fingerprints against a database. The application also supports adding new songs to the fingerprint database.

![image](https://github.com/user-attachments/assets/9812ccf3-962e-4a51-8291-61955d35ade7)


## Features

- **Audio Recording:** Capture audio from your device's microphone.
- **Real-Time Visualization:** Display a live audio waveform during recording.
- **Audio Fingerprinting:** Generate unique fingerprints for audio clips.
- **Song Identification:** Match audio fingerprints with a pre-built database to identify songs.
- **Database Management:** Add new songs to the fingerprint database.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask framework is used for routing and serving content)
- **Audio Processing:** Custom modules (`audio_processing.py` and `fingerprinting.py`) for handling audio capture and generating fingerprints.
- **Matching Logic:** Functions in `matcher.py` to compare fingerprints and identify songs.

## File Structure

- `app.py` - Main application file that starts the server and defines routes.
- `matcher.py` - Contains logic to match audio fingerprints.
- `audio_processing.py` - Handles audio processing and waveform analysis.
- `fingerprinting.py` - Implements the audio fingerprinting algorithm.
- `index.html` - Frontend interface for recording and interacting with the application.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/EgemenErin/ShazamAlgorithm.git
   cd ShazamAlgorithm
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   If a `requirements.txt` file is available, run:
   ```bash
   pip install -r requirements.txt
   ```
   Otherwise, ensure that you have installed all necessary libraries (such as Flask, NumPy, and any audio processing libraries used in the project).

## Usage

1. **Start the Application:**
   ```bash
   python app.py
   ```

2. **Access the Application:**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. **Using the Interface:**
   - Click **Start Recording** to begin capturing audio.
   - Click **Stop Recording** to end the recording session.
   - Click **Identify Song** to process the recording and find a match in the database.
   - Optionally, input a song name and click **Add to Database** to save new audio fingerprints for future identification.

## Contributing

Contributions are welcome! If you have ideas, suggestions, or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

This project was inspired by audio recognition technologies like Shazam and aims to provide a simple demonstration of audio fingerprinting and matching.

---

Feel free to adjust any section as your project evolves or based on additional details in your code files.
