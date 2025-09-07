import numpy as np
import soundfile as sf
from scipy.signal import welch, lfilter

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
        den = np.sum(psd)
        if den <= 0:
            return 0.0
        return float(np.sum(freqs * psd) / den)

    @staticmethod
    def spectral_rolloff(freqs, psd, roll_percent=0.85):
        cumulative = np.cumsum(psd)
        total = cumulative[-1] if cumulative.size else 0.0
        if total <= 0:
            return 0.0
        threshold = roll_percent * total
        idx = np.searchsorted(cumulative, threshold)
        idx = np.clip(idx, 0, len(freqs) - 1)
        return float(freqs[idx])

    @staticmethod
    def zero_crossing_rate(data, frame_size=1024, hop=512):
        if len(data) < frame_size:
            return 0.0
        frames = []
        for i in range(0, len(data) - frame_size + 1, hop):
            frame = data[i:i+frame_size]
            zc = np.mean(np.abs(np.diff(np.signbit(frame))).astype(np.float32))
            frames.append(zc)
        if not frames:
            return 0.0
        return float(np.mean(frames))

    @staticmethod
    def rms_dbfs(data):
        rms = np.sqrt(np.mean(np.square(data))) + 1e-12
        return float(20 * np.log10(rms))

    @staticmethod
    def crest_factor_db(data):
        peak = np.max(np.abs(data)) + 1e-12
        rms = np.sqrt(np.mean(np.square(data))) + 1e-12
        return float(20 * np.log10(peak / rms))

    @staticmethod
    def dynamic_range_db(data, frame_size=2048, hop=1024):
        if len(data) < frame_size:
            return 0.0
        rms_vals = []
        for i in range(0, len(data) - frame_size + 1, hop):
            frame = data[i:i+frame_size]
            rms = np.sqrt(np.mean(frame ** 2)) + 1e-12
            rms_vals.append(20 * np.log10(rms))
        if not rms_vals:
            return 0.0
        low = np.percentile(rms_vals, 5)
        high = np.percentile(rms_vals, 95)
        return float(high - low)

    @staticmethod
    def signal_to_noise_ratio_db(data, frame_size=4096, hop=2048):
        if len(data) < frame_size:
            return 0.0
        rms_frames = []
        for i in range(0, len(data) - frame_size + 1, hop):
            frame = data[i:i+frame_size]
            rms = np.sqrt(np.mean(frame ** 2)) + 1e-12
            rms_frames.append(rms)
        if not rms_frames:
            return 0.0
        rms_frames = np.array(rms_frames)
        noise = np.percentile(rms_frames, 20)
        signal = np.percentile(rms_frames, 80)
        if noise <= 0:
            return 0.0
        return float(20 * np.log10(signal / noise))

    @staticmethod
    def a_weighting_db(freqs):
        f = np.array(freqs, dtype=np.float64)
        f2 = f * f
        ra_num = (12200**2) * (f2**2)
        ra_den = (f2 + 20.6**2) * np.sqrt((f2 + 107.7**2) * (f2 + 737.9**2)) * (f2 + 12200**2)
        ra = ra_num / (ra_den + 1e-30)
        a_db = 2.0 + 20 * np.log10(ra + 1e-30)
        return a_db

    @staticmethod
    def apply_a_weighting_to_psd(freqs, psd):
        a_db = AudioProcessor.a_weighting_db(freqs)
        a_lin_amp = 10 ** (a_db / 20.0)
        psd_aw = psd * (a_lin_amp ** 2)
        return psd_aw

