import numpy as np
from constants import BANDS, WEIGHTS, TARGETS
from audio_processor import AudioProcessor

class AudioAnalyzer:
    @staticmethod
    def score_linear(value, target, tol):
        diff = abs(value - target)
        if diff <= tol:
            return 100.0
        if diff >= 2 * tol:
            return 0.0
        return 100.0 * (1 - (diff - tol) / tol)

    @staticmethod
    def evaluate_psd(freqs, psd):
        metrics = {}
        for name, (f1, f2) in BANDS.items():
            metrics[name] = AudioProcessor.band_power_db(freqs, psd, f1, f2)

        metrics['flatness'] = AudioProcessor.spectral_flatness(psd)
        metrics['centroid'] = AudioProcessor.spectral_centroid(freqs, psd)

        scores = {}
        for name in metrics:
            target, tol = TARGETS.get(name, (0, 1))
            scores[name] = AudioAnalyzer.score_linear(metrics[name], target, tol)

        total = sum(scores[k] * WEIGHTS[k] for k in scores)
        return metrics, scores, total

    @staticmethod
    def generate_report(metrics, scores, total, filename, fs):
        report = []
        report.append(f"Audio Analysis Report: {filename}")
        report.append(f"Sample Rate: {fs} Hz")
        report.append("\nFrequency Band Levels:")

        for band in BANDS:
            report.append(f"  {band:12}: {metrics[band]:6.1f} dB → {scores[band]:5.1f}/100")

        report.append("\nAdditional Metrics:")
        report.append(f"  Spectral Flatness: {metrics['flatness']:6.3f} → {scores['flatness']:5.1f}/100")
        report.append(f"  Spectral Centroid: {metrics['centroid']:7.0f} Hz → {scores['centroid']:5.1f}/100")

        max_freq = fs / 2
        report.append(f"\nFrequency Range: 10 Hz - {max_freq:.0f} Hz")

        report.append(f"\nOverall Score: {total:5.1f}/100")

        return "\n".join(report)
