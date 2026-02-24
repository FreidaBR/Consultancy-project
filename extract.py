import whisper
import soundfile as sf
import numpy as np
import os
import json

WAV_FOLDER  = "wav"
FLAC_FOLDER = "flac"
OUTPUT_FOLDER = "transcripts"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MODEL_SIZE = "base"
print(f"Loading Whisper model: {MODEL_SIZE}...")
model = whisper.load_model(MODEL_SIZE)
print("Model loaded.\n")

results = {}

def transcribe_audio(audio, sr, model):
    # Whisper expects float32 at 16kHz
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32)
    if sr != 16000:
        import librosa
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    result = model.transcribe(audio, language="en")
    return result["text"].strip()

def get_files(folder, extensions):
    return {
        os.path.splitext(f)[0]: os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(extensions)
    }

wav_files  = get_files(WAV_FOLDER,  (".wav",))
flac_files = get_files(FLAC_FOLDER, (".flac",))

# Union of all base names across both folders
all_base_names = sorted(set(wav_files) | set(flac_files))

for base_name in all_base_names:
    # Prefer WAV, fall back to FLAC
    if base_name in wav_files:
        audio_path = wav_files[base_name]
        fmt = "WAV"
    else:
        audio_path = flac_files[base_name]
        fmt = "FLAC"

    print(f"Transcribing [{fmt}]: {os.path.basename(audio_path)}")
    try:
        audio, sr = sf.read(audio_path, dtype="float32")

        # If stereo, mix down to mono
        if audio.ndim == 2:
            audio = audio.mean(axis=1)

        text = transcribe_audio(audio, sr, model)

        txt_path = os.path.join(OUTPUT_FOLDER, base_name + ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        results[base_name] = {"status": "ok", "source": fmt, "text": text}
        print(f"  ✓ Done → {txt_path}\n")

    except Exception as e:
        results[base_name] = {"status": "failed", "source": fmt, "error": str(e)}
        print(f"  ✗ Failed: {e}\n")

# Combined JSON
with open(os.path.join(OUTPUT_FOLDER, "all_transcripts.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Combined readable TXT
with open(os.path.join(OUTPUT_FOLDER, "all_transcripts.txt"), "w", encoding="utf-8") as f:
    for name, data in results.items():
        f.write(f"{'='*60}\n")
        f.write(f"File: {name}  [{data['source']}]\n")
        f.write(f"{'='*60}\n")
        f.write(data["text"] if data["status"] == "ok" else f"[FAILED: {data['error']}]")
        f.write("\n\n")

print("All done! Transcripts saved to 'transcripts/'")