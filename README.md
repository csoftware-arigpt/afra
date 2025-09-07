# 🎧 Audio Frequency Response Analyzer

A Python-based toolkit for **analyzing audio files** and evaluating their **frequency response** in the **10 Hz – 40 kHz** range.  
Designed for audio engineers, researchers, and enthusiasts who want **precise spectral insights** and **visual feedback**.

---

## ✨ Features

- **Spectral Analysis** – Calculates **Power Spectral Density (PSD)** using FFT.
- **Pro Quality Scoring** – Automated evaluation of frequency response using a **multi-metric weighted scoring system**.
- **Multiple Visualizations** – Spectrum plots, radar charts, and waterfall spectrograms.
- **Customizable Themes** – Dark, light, and high-contrast modes.
- **Export Options** – Save plots as high-resolution images for reports or documentation.

---

## 📦 Installation

1. Ensure **Python 3.7+** is installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Basic Analysis  

```bash
python main.py audiofile.wav
```

### Advanced Options  

```bash
python main.py audiofile.wav \
    --n_fft 8192 \          # FFT window size  
    --overlap 0.75 \        # Window overlap ratio (0–1)  
    --output plot.png \     # Save plot to file  
    --radar \               # Generate radar plot  
    --waterfall \           # Generate waterfall spectrogram  
    --theme dark            # Visualization theme
```

---

## 📊 Output Metrics

The analyzer evaluates multiple **objective and perceptual** metrics:

| Metric | Description | Score Range | Interpretation |
|--------|-------------|-------------|----------------|
| **Spectral Flatness** | Measures uniformity of frequency response | 0–20 | Higher = flatter, more neutral |
| **High-Frequency Extension** | Evaluates content beyond 20 kHz | 0–20 | Higher = better ultrasonic preservation |
| **Spectral Roll-off** | Assesses smoothness of high-frequency decay | 0–20 | Higher = smoother roll-off |
| **Noise Floor** | Measures noise level in 20–40 kHz range | 0–20 | Higher = lower noise |
| **Artifacts** | Detects unwanted spectral anomalies | 0–20 | Higher = cleaner signal |
| **Total Score** | Weighted average of all metrics | 0–100 | Overall quality indicator |

---

## 📈 Score Interpretation

| Score Range | Quality Level | Description |
|-------------|--------------|-------------|
| **90–100** | Excellent | Exceptional frequency response, minimal issues |
| **80–89** | Very Good | High quality with minor imperfections |
| **70–79** | Good | Solid performance, some limitations |
| **60–69** | Fair | Average performance, noticeable issues |
| **50–59** | Poor | Below average, significant problems |
| **0–49** | Very Poor | Severe frequency response issues |

---

## 🎵 Supported Formats

Any audio format supported by **SciPy** and **SoundFile**, including:
- WAV
- MP3
- FLAC
- AIFF
- OGG

---

## 📌 Example

```bash
python main.py track.wav --n_fft 16384 --overlap 0.8 --theme light --output analysis.png
```

This will:
- Perform high-resolution spectral analysis
- Apply the pro scoring model
- Save a **light-themed** spectrum plot to `analysis.png`
