# `Audio Frequency Response Analyzer`

`A Python-based tool for analyzing audio files and evaluating their frequency
response characteristics in the 10-40kHz range.`

## `Features`

- `Spectral Analysis: Power Spectral Density (PSD) calculation using FFT`
- `Quality Assessment: Automated evaluation of frequency response using a
  5-metric scoring system`
- `Multiple Visualizations: Spectrum plots, radar charts, and waterfall
  spectrograms`
- `Theme Support: Dark, light, and high-contrast visualization themes`
- `Export Capabilities: Save plots as high-resolution images`

## `Installation`

1.  `Ensure Python 3.7+ is installed`
2.  `Install required dependencies:`

```bash
**pip install -r requirements.txt**
```
## `Usage`

`Basic Analysis`

```bash
**python main.py audiofile.wav**
```
## `Advanced Options`

```bash
**python main.py audiofile.wav \**
**    --n_fft 8192 \          # FFT window size**
**    --overlap 0.75 \        # Window overlap ratio (0-1)**
**    --output plot.png \     # Save plot to file**
**    --radar \               # Generate radar plot**
**    --waterfall \           # Generate waterfall spectrogram**
**    --theme dark            # Visualization theme**
```
## `Output Metrics`

`The analysis evaluates five key metrics:`


|Metric     |Description                                               |Score Range|Interpretation                                               |
|-----------|----------------------------------------------------------|-----------|-------------------------------------------------------------|
|`Flatness` |`Measures frequency response uniformity across the spectrum`|`0-20`     |`Higher scores indicate flatter, more neutral response`      |
|`Extension`|`Evaluates high-frequency extension beyond 20kHz`         |`0-20`     |`Higher scores indicate better ultrasonic content preservation`|
|`Roll-off` |`Analyzes high-frequency roll-off characteristics`        |`0-20`     |`Higher scores indicate smoother, more gradual roll-off`     |
|`Noise Floor`|`Measures noise level in high-frequency range (20-40kHz)` |`0-20`     |`Higher scores indicate lower noise floor`                   |
|`Artifacts`|`Detects unwanted artifacts and anomalies in the spectrum`|`0-20`     |`Higher scores indicate fewer artifacts and cleaner signal`  |
|`Total Score`|`Overall quality assessment (weighted average of metrics)`|`0-100`    |`Comprehensive quality indicator`                            |

## `Score Interpretation Guide`


|Score Range|Quality Level|Description                                       |
|-----------|-------------|--------------------------------------------------|
|`90-100`   |`Excellent`  |`Exceptional frequency response with minimal issues`|
|`80-89`    |`Very Good`  |`High-quality performance with minor imperfections`|
|`70-79`    |`Good`       |`Solid performance with some noticeable limitations`|
|`60-69`    |`Fair`       |`Average performance with several limitations`    |
|`50-59`    |`Poor`       |`Below average with significant issues`           |
|`0-49`     |`Very Poor`  |`Severe frequency response problems`              |

## `Supported Formats`

`All audio formats readable by SciPy (WAV, MP3, FLAC, etc.).`

