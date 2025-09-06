import numpy as np
import soundfile as sf
from scipy.signal import welch

class AudioProcessor:
    @staticmethod
    def load_audio(filename):
        data, fs = sf.read(filename)
        if data.ndim > 1:
            data = data.mean(axis=1)
        return data, fs

    @staticmethod
    def compute_psd(data, fs, n_fft=4096, overlap=0.5):
        n_ov = int(n_fft * overlap)
        freqs, psd = welch(
            data,
            fs=fs,
            window='hann',
            nperseg=n_fft,
            noverlap=n_ov,
            scaling='spectrum'
        )
        return freqs, psd

    @staticmethod
    def band_power_db(freqs, psd, f_low, f_high):
        mask = (freqs >= f_low) & (freqs <= f_high)
        if not np.any(mask):
            return -np.inf
        power = np.trapz(psd[mask], freqs[mask])
        return 10 * np.log10(power + 1e-12)

    @staticmethod
    def spectral_flatness(psd):
        positive_psd = psd[psd > 0]
        if len(positive_psd) == 0:
            return 0.0
        am = np.mean(positive_psd)
        gm = np.exp(np.mean(np.log(positive_psd)))
        return gm / am

    @staticmethod
    def spectral_centroid(freqs, psd):
        if np.sum(psd) <= 0:
            return 0.0
        return np.sum(freqs * psd) / np.sum(psd)
