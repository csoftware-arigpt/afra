#!/usr/bin/env python3
import argparse
import os
import sys
import numpy as np
import matplotlib
backends = ['Qt5Agg', 'Qt4Agg', 'TkAgg', 'MacOSX']
for backend in backends:
    try:
        matplotlib.use(backend)
        import matplotlib.pyplot as plt
        break
    except:
        continue

from audio_processor import AudioProcessor
from analyzer import AudioAnalyzer
from visualizer import AudioVisualizer

def main():
    parser = argparse.ArgumentParser(description="Audio file analysis and frequency evaluation (10–40 kHz range, pro scoring)")
    parser.add_argument("filename", help="Path to audio file")
    parser.add_argument("--n_fft", type=int, default=8192, help="FFT window length")
    parser.add_argument("--overlap", type=float, default=0.75, help="Window overlap ratio (0–1)")
    parser.add_argument("--output", "-o", help="Save plot to file")
    parser.add_argument("--radar", action="store_true", help="Generate radar plot")
    parser.add_argument("--waterfall", action="store_true", help="Generate waterfall plot")
    parser.add_argument("--theme", default="dark", choices=["dark", "light", "high_contrast"],
                        help="Visualization theme")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found")
        sys.exit(1)

    try:
        visualizer = AudioVisualizer(theme=args.theme)

        data, fs = AudioProcessor.load_audio(args.filename)

        freqs, psd_aw, metrics, scores, total = AudioAnalyzer.evaluate(
            data, fs, n_fft=args.n_fft, overlap=args.overlap
        )

        psd_db = 10 * np.log10(psd_aw + 1e-12)

        report = AudioAnalyzer.generate_report(metrics, scores, total, os.path.basename(args.filename), fs)
        print(report)

        if args.waterfall and hasattr(visualizer, "create_waterfall_plot"):
            fig = visualizer.create_waterfall_plot(freqs, psd_db, os.path.basename(args.filename), fs)
        elif args.radar and hasattr(visualizer, "create_radar_plot"):
            fig = visualizer.create_radar_plot(scores)
        else:
            fig = visualizer.create_spectrum_plot(freqs, psd_db, metrics, scores, total,
                                                  os.path.basename(args.filename), fs)

        if args.output:
            plt.savefig(args.output, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {args.output}")
        else:
            plt.show()

    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

