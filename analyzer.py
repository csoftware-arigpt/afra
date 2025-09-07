import numpy as np
from constants import BANDS, WEIGHTS, TARGETS
from audio_processor import AudioProcessor

class AudioAnalyzer:
    METRIC_NAMES = {
        'flatness': 'Spectral Flatness',
        'centroid': 'Spectral Centroid',
        'rolloff_85': 'Spectral Rolloff (85%)',
        'zcr': 'Zero Crossing Rate',
        'snr_db': 'Signal-to-Noise Ratio (dB)',
        'crest_db': 'Crest Factor (dB)',
        'dyn_range_db': 'Dynamic Range (dB)',
        'loudness_dbfs': 'Loudness (dBFS)'
    }

    @staticmethod
    def score_smooth(value, target, tol):
        diff = abs(value - target)
        if tol <= 0:
            return 0.0
        if diff <= tol:
            return 100.0
        if diff >= 2 * tol:
            return 0.0
        r = (diff - tol) / tol
        return 50.0 * (1 + np.cos(np.pi * r))

    @staticmethod
    def clamp(x, lo=0.0, hi=100.0):
        return float(max(lo, min(hi, x)))

    @staticmethod
    def evaluate(data, fs, n_fft=4096, overlap=0.5):
        freqs, psd = AudioProcessor.compute_psd(data, fs, n_fft=n_fft, overlap=overlap)
        psd_aw = AudioProcessor.apply_a_weighting_to_psd(freqs, psd)
        raw_metrics = {}
        for name, (f1, f2) in BANDS.items():
            raw_metrics[name] = float(AudioProcessor.band_power_db(freqs, psd_aw, f1, f2))
        raw_metrics['flatness'] = float(AudioProcessor.spectral_flatness(psd_aw))
        raw_metrics['centroid'] = float(AudioProcessor.spectral_centroid(freqs, psd_aw))
        raw_metrics['rolloff_85'] = float(AudioProcessor.spectral_rolloff(freqs, psd_aw, 0.85))
        raw_metrics['zcr'] = float(AudioProcessor.zero_crossing_rate(data))
        raw_metrics['snr_db'] = float(AudioProcessor.signal_to_noise_ratio_db(data))
        raw_metrics['crest_db'] = float(AudioProcessor.crest_factor_db(data))
        raw_metrics['dyn_range_db'] = float(AudioProcessor.dynamic_range_db(data))
        raw_metrics['loudness_dbfs'] = float(AudioProcessor.rms_dbfs(data))
        raw_scores = {}
        for name, value in raw_metrics.items():
            target, tol = TARGETS.get(name, (0.0, 1.0))
            raw_scores[name] = AudioAnalyzer.clamp(AudioAnalyzer.score_smooth(value, target, tol))
        wsum = sum(WEIGHTS.get(k, 0.0) for k in raw_scores.keys())
        wnorm = {k: WEIGHTS.get(k, 0.0) / (wsum if wsum > 0 else 1.0) for k in raw_scores.keys()}
        total = sum(raw_scores[k] * wnorm[k] for k in raw_scores.keys())
        metrics_hr = {}
        scores_hr = {}
        for key, val in raw_metrics.items():
            if key in BANDS:
                display_name = key.title().replace('-', ' ')
            else:
                display_name = AudioAnalyzer.METRIC_NAMES.get(key, key)
            metrics_hr[display_name] = val
            scores_hr[display_name] = raw_scores[key]
        return freqs, psd_aw, metrics_hr, scores_hr, float(round(total, 2))

    @staticmethod
    def generate_report(metrics, scores, total, filename, fs):
        report = []
        report.append(f"Audio Analysis Report: {filename}")
        report.append(f"Sample Rate: {fs} Hz")
        report.append("\nFrequency Band Levels (A-weighted):")
        for band in BANDS:
            display_name = band.title().replace('-', ' ')
            report.append(f"  {display_name:20}: {metrics[display_name]:8.2f} dB → {scores[display_name]:6.2f}/100")
        report.append("\nAdditional Metrics:")
        extra = [k for k in metrics.keys() if k not in [b.title().replace('-', ' ') for b in BANDS]]
        for k in extra:
            val = metrics[k]
            sc = scores[k]
            unit = "Hz" if "Centroid" in k or "Rolloff" in k else "dB" if any(x in k for x in ["dB", "Loudness"]) else ""
            report.append(f"  {k:25}: {val:10.2f} {unit} → {sc:6.2f}/100")
        max_freq = fs / 2
        report.append(f"\nFrequency Range: 10 Hz - {max_freq:.0f} Hz")
        report.append(f"\nOverall Score: {total:6.2f}/100")
        return "\n".join(report)
