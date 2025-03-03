document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const identifyButton = document.getElementById('identifyButton');
    const addToDbButton = document.getElementById('addToDbButton');
    const songNameInput = document.getElementById('songName');
    const audioPlayback = document.getElementById('audioPlayback');
    const visualizer = document.getElementById('visualizer');
    const timerDisplay = document.getElementById('timer');
    const resultContainer = document.getElementById('result');

    // Canvas context for visualization
    const canvasCtx = visualizer.getContext('2d');

    // Variables
    let mediaRecorder;
    let audioChunks = [];
    let audioBlob;
    let audioUrl;
    let startTime;
    let timerInterval;
    let audioContext;
    let analyser;
    let dataArray;
    let source;
    let lastRecordingFilename;

    // Check if browser supports getUserMedia
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Your browser does not support audio recording');
        return;
    }

    // Set up canvas size
    function setupCanvas() {
        visualizer.width = visualizer.clientWidth;
        visualizer.height = visualizer.clientHeight;
    }

    // Initialize audio context
    function initAudioContext() {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 2048;
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
    }

    // Start visualization
    function startVisualization(stream) {
        source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
        drawVisualizer();
    }

    // Draw visualizer
    function drawVisualizer() {
        requestAnimationFrame(drawVisualizer);

        analyser.getByteTimeDomainData(dataArray);

        canvasCtx.fillStyle = 'rgb(248, 249, 250)';
        canvasCtx.fillRect(0, 0, visualizer.width, visualizer.height);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = 'rgb(52, 152, 219)';
        canvasCtx.beginPath();

        const sliceWidth = visualizer.width / dataArray.length;
        let x = 0;

        for (let i = 0; i < dataArray.length; i++) {
            const v = dataArray[i] / 128.0;
            const y = v * visualizer.height / 2;

            if (i === 0) {
                canvasCtx.moveTo(x, y);
            } else {
                canvasCtx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        canvasCtx.lineTo(visualizer.width, visualizer.height / 2);
        canvasCtx.stroke();
    }

    // Update timer display
    function updateTimer() {
        const now = Date.now();
        const diff = now - startTime;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const formattedSeconds = (seconds % 60).toString().padStart(2, '0');
        const formattedMinutes = minutes.toString().padStart(2, '0');
        timerDisplay.textContent = `${formattedMinutes}:${formattedSeconds}`;
    }

    // Start recording
    function startRecording() {
        audioChunks = [];

        // Reset UI
        resultContainer.innerHTML = '';

        // Get microphone permissions
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                // Initialize audio visualization
                if (!audioContext) {
                    initAudioContext();
                }
                startVisualization(stream);

                // Create media recorder
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = e => {
                    audioChunks.push(e.data);
                };

                mediaRecorder.onstop = () => {
                    // Create blob from chunks
                    audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    audioUrl = URL.createObjectURL(audioBlob);

                    // Set to audio player
                    audioPlayback.src = audioUrl;

                    // Enable buttons
                    identifyButton.disabled = false;
                    songNameInput.disabled = false;

                    // Show result container
                    resultContainer.innerHTML = '<p>Recording completed. You can now identify or add to database.</p>';
                };

                // Start recording
                mediaRecorder.start();

                // Update UI
                recordButton.disabled = true;
                stopButton.disabled = false;

                // Start timer
                startTime = Date.now();
                timerInterval = setInterval(updateTimer, 1000);
                updateTimer();
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                resultContainer.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
            });
    }

    // Stop recording
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();

            // Stop all tracks on the active stream
            mediaRecorder.stream.getTracks().forEach(track => track.stop());

            // Update UI
            recordButton.disabled = false;
            stopButton.disabled = true;

            // Stop timer
            clearInterval(timerInterval);
        }
    }

    // Identify song
    function identifySong() {
        if (!audioBlob) {
            return;
        }

        resultContainer.innerHTML = '<p>Identifying song...</p>';

        // Convert blob to base64
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = function() {
            const base64data = reader.result;

            // Send to server
            fetch('/identify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    audio: base64data
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultContainer.innerHTML = `
                        <p>Identification result:</p>
                        <h3>${data.result}</h3>
                        <p>Confidence: ${data.confidence}</p>
                    `;
                } else {
                    resultContainer.innerHTML = `<p class="error-message">Error: ${data.message}</p>`;
                }
            })
            .catch(error => {
                console.error('Error identifying song:', error);
                resultContainer.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
            });
        };
    }

    // Save recording and add to database
    function addToDatabase() {
        if (!audioBlob || !songNameInput.value.trim()) {
            return;
        }

        const songName = songNameInput.value.trim();
        resultContainer.innerHTML = `<p>Adding "${songName}" to database...</p>`;

        // First save the recording
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = function() {
            const base64data = reader.result;

            // Save recording
            fetch('/save-recording', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    audio: base64data
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    lastRecordingFilename = data.filename;

                    // Now add to database
                    return fetch('/add-to-db', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            filename: lastRecordingFilename,
                            songName: songName
                        })
                    });
                } else {
                    throw new Error(data.message);
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultContainer.innerHTML = `<p class="success-message">${data.message}</p>`;
                    songNameInput.value = '';
                    addToDbButton.disabled = true;
                } else {
                    resultContainer.innerHTML = `<p class="error-message">Error: ${data.message}</p>`;
                }
            })
            .catch(error => {
                console.error('Error adding to database:', error);
                resultContainer.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
            });
        };
    }

    // Event listeners
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    identifyButton.addEventListener('click', identifySong);
    addToDbButton.addEventListener('click', addToDatabase);

    // Enable Add to Database button when song name is entered
    songNameInput.addEventListener('input', function() {
        addToDbButton.disabled = !this.value.trim();
    });

    // Set up canvas on load and resize
    setupCanvas();
    window.addEventListener('resize', setupCanvas);
});