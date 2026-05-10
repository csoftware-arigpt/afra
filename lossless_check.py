import numpy as np


class LosslessChecker:
    CODEC_SIGNATURES = [
        (21000.0, float('inf'), 'True lossless (~22 kHz extent)'),
        (20000.0, 21000.0, 'MP3 256-320 kbps'),
        (19000.0, 20000.0, 'MP3 V0 / 192 kbps'),
        (18000.0, 19000.0, 'MP3 V2'),
        (16000.0, 18000.0, 'MP3 128 kbps or AAC ~128 kbps'),
        (0.0, 16000.0, 'Heavy lossy or band-limited'),
    ]

    @staticmethod
    def estimate_cutoff(freqs: np.ndarray, psd: np.ndarray, ref_low: float = 1000.0,
                        ref_high: float = 5000.0, drop_db: float = 60.0) -> float:
        if len(freqs) == 0 or len(psd) == 0:
            return 0.0
        ref_mask = (freqs >= ref_low) & (freqs <= ref_high) & (psd > 0)
        if not np.any(ref_mask):
            return 0.0
        ref_db = 10.0 * np.log10(np.median(psd[ref_mask]))
        threshold_db = ref_db - drop_db
        psd_db = 10.0 * np.log10(np.maximum(psd, 1e-30))
        above_ref = freqs > ref_high
        candidates = np.where(above_ref & (psd_db >= threshold_db))[0]
        if candidates.size == 0:
            return float(ref_high)
        return float(freqs[candidates.max()])

    @staticmethod
    def detect_brickwall(freqs: np.ndarray, psd: np.ndarray, cutoff_hz: float,
                         span_hz: float = 1000.0) -> float:
        if cutoff_hz <= 0:
            return 0.0
        below_mask = (freqs >= cutoff_hz - span_hz) & (freqs <= cutoff_hz)
        above_mask = (freqs > cutoff_hz) & (freqs <= cutoff_hz + span_hz)
        if not np.any(below_mask) or not np.any(above_mask):
            return 0.0
        below_db = 10.0 * np.log10(np.maximum(np.median(psd[below_mask]), 1e-30))
        above_db = 10.0 * np.log10(np.maximum(np.median(psd[above_mask]), 1e-30))
        return float(below_db - above_db)

    @staticmethod
    def classify(cutoff_hz: float) -> str:
        for low, high, label in LosslessChecker.CODEC_SIGNATURES:
            if low <= cutoff_hz < high:
                return label
        return 'Unknown'

    @staticmethod
    def analyze(freqs: np.ndarray, psd: np.ndarray, fs: int) -> dict:
        nyquist = fs / 2.0
        if fs < 32000 or nyquist < 20000:
            return {
                'cutoff_hz': 0.0,
                'brickwall_drop_db': 0.0,
                'verdict': 'Inconclusive (sample rate too low)',
                'suspected_format': 'unknown',
                'confidence': 0.0,
            }
        cutoff = LosslessChecker.estimate_cutoff(freqs, psd)
        brick = LosslessChecker.detect_brickwall(freqs, psd, cutoff)
        label = LosslessChecker.classify(cutoff)

        if cutoff >= 21000.0 and brick < 20.0:
            verdict = 'Likely true lossless'
            confidence = 0.85
        elif cutoff >= 21000.0:
            verdict = 'Lossless extent but suspicious brick-wall'
            confidence = 0.55
        elif cutoff >= 20000.0 and brick < 25.0:
            verdict = 'Borderline — soft-rolloff lossless or high-bitrate MP3'
            confidence = 0.50
        else:
            verdict = f'Likely transcode: {label}'
            confidence = 0.65 + min(max(brick, 0.0), 60.0) / 200.0

        return {
            'cutoff_hz': float(cutoff),
            'brickwall_drop_db': float(brick),
            'verdict': verdict,
            'suspected_format': label,
            'confidence': float(min(confidence, 0.99)),
        }
