# 🎙 Audio Transcription Project (Whisper Batch Processing)

This project performs **batch transcription of WAV and FLAC audio files** using OpenAI’s Whisper speech-to-text model.

It automatically:

* Loads audio files from folders
* Converts them to the required format (16kHz, mono, float32)
* Transcribes using Whisper
* Saves individual transcripts
* Generates combined JSON and TXT summary files

---

## 📁 Project Structure

```
Consultancy-project/
│
├── wav/                  # Input WAV files
├── flac/                 # Input FLAC files
├── transcripts/          # Output transcripts (auto-created)
├── extract.py            # Main transcription script
└── README.md
```

---

## ⚙️ Requirements

* Python **3.10** (recommended for Whisper stability)
* pip or uv
* Dependencies:

  * openai-whisper
  * torch
  * soundfile
  * librosa
  * numpy

---

## 🚀 Setup Instructions (Using uv – Recommended)

### 1️⃣ Install Python 3.10

If not installed:

```powershell
uv python install 3.10
```

---

### 2️⃣ Create Virtual Environment

```powershell
uv venv --python 3.10
.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```powershell
uv pip install torch
uv pip install openai-whisper
uv pip install soundfile librosa numpy
```

---

## ▶️ How to Run

Place your audio files inside:

* `wav/` folder for `.wav`
* `flac/` folder for `.flac`

Then run:

```powershell
python extract.py
```

You should see:

```
Loading Whisper model: base...
Model loaded.
Transcribing [WAV]: filename.wav
✓ Done → transcripts/filename.txt
```

---

## 🧠 How It Works

### 1. Model Loading

```python
model = whisper.load_model("base")
```

The script uses the **base Whisper model** for balanced speed and accuracy.

---

### 2. Audio Preprocessing

Whisper expects:

* Mono audio
* 16kHz sample rate
* float32 format

The script:

* Converts stereo to mono
* Resamples to 16kHz (using librosa)
* Converts to float32

---

### 3. Transcription

```python
result = model.transcribe(audio, language="en")
```

Language is forced to English.

---

### 4. Output Files

For each audio file:

```
transcripts/<filename>.txt
```

Additionally:

### 📄 `all_transcripts.json`

Structured machine-readable output:

```json
{
  "filename": {
    "status": "ok",
    "source": "WAV",
    "text": "transcribed text..."
  }
}
```

### 📄 `all_transcripts.txt`

Human-readable combined transcript file:

```
============================================================
File: ExampleFile  [WAV]
============================================================
Transcribed content...
```

---

## 📌 Example Output

Example transcript snippet:

```
File: WhatsApp Audio 2026-01-06 at 7.20.08 PM (1)  [WAV]

One, one, one, one, two, two, three, three, four...
...
Say 100. 100. 100.
```

---

## 🔧 Customization

You can change model size:

```python
MODEL_SIZE = "base"
```

Available options:

* tiny  (fastest, lowest accuracy)
* base  (balanced)
* small
* medium
* large (best accuracy, slowest)

---

## ⚡ Performance Notes

* GPU significantly improves speed (if CUDA-enabled PyTorch is installed)
* CPU-only works but is slower
* Larger models require more RAM

---

## 🛠 Troubleshooting

### ❌ Error: `whisper.py` conflict

If you accidentally install the wrong package:

```powershell
pip uninstall whisper
pip install openai-whisper
```

Make sure only `openai-whisper` is installed.

---

### ❌ Python 3.14 Issues

Whisper + PyTorch may fail on very new Python versions.

Use **Python 3.10** for best stability.

---

## 📈 Possible Improvements

* Add progress bars (tqdm)
* Add timestamps
* Enable GPU acceleration
* Switch to faster-whisper for speed optimization
* Parallel processing

---