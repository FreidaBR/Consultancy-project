from pydub import AudioSegment
import os

INPUT_FOLDER = "mp3"
OUTPUT_FOLDER = "wav"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".mp3"):
        mp3_path = os.path.join(INPUT_FOLDER, file)

        audio = AudioSegment.from_mp3(mp3_path)

        # make mono
        audio = audio.set_channels(1)

        # set sample rate to 16000 Hz
        audio = audio.set_frame_rate(16000)

        # export as WAV
        wav_name = file.replace(".mp3", ".wav")
        wav_path = os.path.join(OUTPUT_FOLDER, wav_name)

        audio.export(wav_path, format="wav")

        print(f"Converted: {file} → {wav_name}")
