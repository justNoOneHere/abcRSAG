from moviepy.editor import VideoFileClip, AudioFileClip
import os
import random

def combine_video_audio(video_path, audio_path, output_path):
    # Load video clip
    video_clip = VideoFileClip(video_path)

    # Load a random audio clip from the 'a' directory
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith(".mp3")]
    if audio_files:
        random_audio_filename = random.choice(audio_files)
        random_audio_path = os.path.join(audio_directory, random_audio_filename)
        audio_clip = AudioFileClip(random_audio_path)
    else:
        print("No audio files found in the 'a' directory.")
        return

    # Set video clip's audio to the loaded audio clip
    video_clip = video_clip.set_audio(audio_clip)

    # Write the result to a new file
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    # Input directories
    video_directory = "abcRSAG/v"
    audio_directory = "abcRSAG/a"

    # Output directory
    output_directory = "abcRSAG/vc"

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over each video file in the 'v' directory
    for video_filename in os.listdir(video_directory):
        if video_filename.endswith(".mp4"):
            video_path = os.path.join(video_directory, video_filename)

            # Generate output file path in 'vc' directory
            output_filename = os.path.splitext(video_filename)[0] + ".mp4"
            output_path = os.path.join(output_directory, output_filename)

            # Combine video with a random audio file
            combine_video_audio(video_path, audio_directory, output_path)

    print("Process completed.")
