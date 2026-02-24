import miniaudio
import soundfile as sf
import numpy as np
import os

INPUT_FOLDER = "mp3"
WAV_FOLDER = "wav"
FLAC_FOLDER = "flac"

os.makedirs(WAV_FOLDER, exist_ok=True)
os.makedirs(FLAC_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):
    if not file.lower().endswith((".mp3", ".mpeg")):
        continue

    input_path = os.path.join(INPUT_FOLDER, file)
    base_name = os.path.splitext(file)[0]
    wav_path = os.path.join(WAV_FOLDER, base_name + ".wav")
    flac_path = os.path.join(FLAC_FOLDER, base_name + ".flac")

    try:
        decoded = miniaudio.decode_file(
            input_path,
            output_format=miniaudio.SampleFormat.SIGNED16,
            nchannels=1,
            sample_rate=16000
        )
        audio = np.frombuffer(decoded.samples, dtype=np.int16)
        sf.write(wav_path, audio, 16000)
        sf.write(flac_path, audio, 16000)
        print(f"Converted {file} → WAV + FLAC")

    except Exception as e:
        print(f"Failed {file}: {e}")