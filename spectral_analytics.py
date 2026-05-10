import numpy as np


class SpectralAnalytics:
    @staticmethod
    def spectral_spread(freqs: np.ndarray, psd: np.ndarray, centroid: float | None = None) -> float:
        den = float(np.sum(psd))
        if den <= 0:
            return 0.0
        c = centroid if centroid is not None else float(np.sum(freqs * psd) / den)
        var = float(np.sum(((freqs - c) ** 2) * psd) / den)
        return float(np.sqrt(max(var, 0.0)))

    @staticmethod
    def spectral_skewness(freqs: np.ndarray, psd: np.ndarray) -> float:
        den = float(np.sum(psd))
        if den <= 0:
            return 0.0
        c = float(np.sum(freqs * psd) / den)
        var = float(np.sum(((freqs - c) ** 2) * psd) / den)
        sd = float(np.sqrt(max(var, 0.0)))
        if sd <= 0:
            return 0.0
        return float(np.sum(((freqs - c) ** 3) * psd) / (den * sd ** 3))

    @staticmethod
    def spectral_kurtosis(freqs: np.ndarray, psd: np.ndarray) -> float:
        den = float(np.sum(psd))
        if den <= 0:
            return 0.0
        c = float(np.sum(freqs * psd) / den)
        var = float(np.sum(((freqs - c) ** 2) * psd) / den)
        if var <= 0:
            return 0.0
        return float(np.sum(((freqs - c) ** 4) * psd) / (den * var ** 2))

    @staticmethod
    def spectral_entropy(psd: np.ndarray) -> float:
        s = float(np.sum(psd))
        if s <= 0:
            return 0.0
        p = psd / s
        p = p[p > 0]
        if p.size == 0:
            return 0.0
        h = -float(np.sum(p * np.log2(p)))
        h_max = float(np.log2(p.size))
        return h / h_max if h_max > 0 else 0.0

    @staticmethod
    def spectral_slope(freqs: np.ndarray, psd: np.ndarray) -> float:
        mask = (freqs > 0) & (psd > 0)
        if np.count_nonzero(mask) < 2:
            return 0.0
        x = np.log10(freqs[mask])
        y = 10.0 * np.log10(psd[mask])
        slope, _ = np.polyfit(x, y, 1)
        return float(slope)

    @staticmethod
    def spectral_decrease(psd: np.ndarray) -> float:
        if len(psd) < 2:
            return 0.0
        k = np.arange(1, len(psd))
        den = float(np.sum(psd[1:]))
        if den <= 0:
            return 0.0
        num = float(np.sum((psd[1:] - psd[0]) / k))
        return num / den

    @staticmethod
    def spectral_contrast(freqs: np.ndarray, psd: np.ndarray, n_bands: int = 6) -> float:
        if len(psd) == 0 or len(freqs) < 2:
            return 0.0
        f_min = max(float(freqs[1]), 20.0)
        f_max = float(freqs[-1])
        if f_max <= f_min:
            return 0.0
        edges = np.logspace(np.log10(f_min), np.log10(f_max), n_bands + 1)
        contrasts = []
        for i in range(n_bands):
            mask = (freqs >= edges[i]) & (freqs < edges[i + 1])
            if not np.any(mask):
                continue
            band = psd[mask]
            band = band[band > 0]
            if band.size < 2:
                continue
            peak = 10.0 * np.log10(np.percentile(band, 95))
            valley = 10.0 * np.log10(np.percentile(band, 5))
            contrasts.append(peak - valley)
        if not contrasts:
            return 0.0
        return float(np.mean(contrasts))

    @staticmethod
    def spectral_bandwidth(freqs: np.ndarray, psd: np.ndarray, p: int = 2) -> float:
        den = float(np.sum(psd))
        if den <= 0:
            return 0.0
        c = float(np.sum(freqs * psd) / den)
        bw = float(np.sum((np.abs(freqs - c) ** p) * psd) / den) ** (1.0 / p)
        return bw
