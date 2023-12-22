import os
import random
from pydub import AudioSegment
from pydub.generators import Sine
import uuid

def generate_random_beep():
    # Random frequency for the beep (you can adjust the range as needed)
    frequency = random.randint(100, 2000)
    
    # Random duration for the beep (you can adjust the range as needed)
    duration = random.uniform(0.1, 5)
    
    # Generate a sine wave for the beep
    beep = Sine(frequency).to_audio_segment(duration=duration * 1000)  # Convert duration to milliseconds
    
    return beep

def generate_random_audio(duration=10, num_beeps=20):
    audio = AudioSegment.silent(duration=duration * 1000)  # Convert duration to milliseconds

    for _ in range(num_beeps):
        start_time = random.uniform(0, duration)
        beep = generate_random_beep()
        audio = audio.overlay(beep, position=int(start_time * 1000))  # Convert start_time to milliseconds

    return audio

def main():
    num_files = int(input("Enter the number of audio files to generate: "))

    for i in range(num_files):
        output_file = f"abcRSAG/a/{str(uuid.uuid4())}.mp3"
        random_audio = generate_random_audio()
        random_audio.export(output_file, format="mp3")
        print(f"Random audio with beeps generated and saved to {output_file}")

if __name__ == "__main__":
    main()
