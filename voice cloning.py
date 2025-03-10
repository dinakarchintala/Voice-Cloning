# -*- coding: utf-8 -*-
"""Untitled28.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n7-wuH89boEKkyX1NDcXlYYHKDG9me-Y
"""

pip install --upgrade elevenlabs

import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from IPython.display import Audio
import io

# Load environment variables
load_dotenv()

# Get API key from environment or manually set it
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    api_key = "Add your API key"  # Replace with your actual API key

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)

# Generate speech using the text_to_speech method
audio = client.text_to_speech.convert(
    text="   When the world is in brink of chaos a hero will raise",
    voice_id="WjBaXAOzAWIbnih1I9Ct",  # Replace with a valid voice ID #WjBaXAOzAWIbnih1I9Ct
    model_id="eleven_monolingual_v1"
)

# Convert the generator to bytes
audio_bytes = b''.join([bytes(chunk) for chunk in audio])

# Save the audio to a file
with open("output.wav", "wb") as f:
    f.write(audio_bytes)

# Play the audio in Colab
Audio("output.wav")

!pip install pydub

import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from IPython.display import Audio
from google.colab import files
from pydub import AudioSegment  # Ensure this is installed: pip install pydub

# Load environment variables
load_dotenv()

# Get API key from environment or manually set it
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    api_key = "Add your API key"  # Replace with your actual API key

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)

# Step 1: Upload audio files for cloning
print("Please upload your audio files (MP3 or WAV format, at least 60 sec long):")
uploaded_files = files.upload()

# Get the uploaded file names
audio_file_paths = list(uploaded_files.keys())

# Step 1.5: Convert MP3 to WAV if necessary
converted_files = []
for file_path in audio_file_paths:
    if file_path.endswith('.mp3'):
        # Load and convert MP3 to WAV
        audio = AudioSegment.from_mp3(file_path)
        wav_file_path = file_path.replace('.mp3', '.wav')
        audio = audio.set_frame_rate(22050).set_channels(1)  # Ensure correct format
        audio.export(wav_file_path, format='wav')
        converted_files.append(wav_file_path)
        print(f"Converted '{file_path}' to '{wav_file_path}'")
    else:
        converted_files.append(file_path)

# Step 2: Clone the voice using the uploaded audio files
voice_name = "My Cloned Voice"
voice_id = None  # Initialize

try:
    voice = client.voices.add(
        name=voice_name,
        files=converted_files,
        description="My cloned voice for testing."
    )
    voice_id = voice.id  # Extract the correct voice ID
    print(f"Voice cloned successfully! Voice ID: {voice_id}")

except Exception as e:
    print(f"Error cloning voice: {e}")

# Step 3: Verify and Use the Cloned Voice
if voice_id:
    print("Fetching all voices to verify cloning...")
    voices = client.voices.get_all()

    for v in voices:
        print(f"Available Voice: {v.name} (ID: {v.id})")
        if v.name == voice_name:
            voice_id = v.id  # Ensure we use the correct voice_id
            break

    # Step 4: Generate Speech with Cloned Voice
    text_to_speak = "Hello, this is my cloned voice speaking."
    try:
        print(f"Using Voice ID: {voice_id} for speech generation")
        audio = client.text_to_speech.convert(
            text=text_to_speak,
            voice_id=voice_id,
            model_id="eleven_monolingual_v1"
        )

        # Convert the generator to bytes
        audio_bytes = b''.join([bytes(chunk) for chunk in audio])

        # Save the audio to a file
        output_file = "output_cloned.wav"
        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        print("Audio generated successfully with cloned voice!")

    except Exception as e:
        print(f"Error generating speech: {e}")
else:
    print("Voice ID is not available. Check if voice cloning was successful.")

# Step 5: Play the generated audio in Colab
Audio("output_cloned.wav")
