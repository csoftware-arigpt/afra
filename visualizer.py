import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import spectrogram
from constants import BANDS


class AudioVisualizer:
    def __init__(self, theme: str = 'dark') -> None:
        self.theme = theme
        self._setup_theme()

    def _setup_theme(self) -> None:
        if self.theme == 'light':
            plt.style.use('default')
            self.colors = {
                'background': '#FFFFFF',
                'grid': '#E0E0E0',
                'text': '#212121',
                'accent': '#2196F3',
                'secondary': '#4CAF50',
                'warning': '#FF9800',
            }
        elif self.theme == 'high_contrast':
            plt.style.use('default')
            self.colors = {
                'background': '#FFFFFF',
                'grid': '#CCCCCC',
                'text': '#000000',
                'accent': '#1976D2',
                'secondary': '#388E3C',
                'warning': '#D32F2F',
            }
        else:
            plt.style.use('dark_background')
            self.colors = {
                'background': '#000000',
                'grid': '#444444',
                'text': '#FFFFFF',
                'accent': '#4FC3F7',
                'secondary': '#81C784',
                'warning': '#FF8A65',
            }

    @staticmethod
    def _format_value(name: str, value: float) -> str:
        if any(x in name for x in ("Spread", "Bandwidth", "Centroid", "Rolloff")):
            return f"{value:>9.0f} Hz"
        if "Slope" in name:
            return f"{value:>+8.2f} dB/dec"
        if "Contrast" in name:
            return f"{value:>+8.2f} dB"
        return f"{value:>9.4f}"

    LABEL_WIDTH = 19
    VALUE_WIDTH = 22

    @staticmethod
    def _wrap_value(value: str, width: int) -> list[str]:
        if len(value) <= width:
            return [value]
        chunks: list[str] = []
        remaining = value
        while len(remaining) > width:
            split_at = remaining.rfind(' ', 0, width)
            if split_at <= 0:
                split_at = width
            chunks.append(remaining[:split_at].rstrip())
            remaining = remaining[split_at:].lstrip()
        if remaining:
            chunks.append(remaining)
        return chunks

    def _format_row(self, label: str, value: str) -> list[str]:
        chunks = self._wrap_value(value, self.VALUE_WIDTH)
        first = f"{label:<{self.LABEL_WIDTH}}: {chunks[0]}"
        rest = [f"{'':<{self.LABEL_WIDTH}}  {c}" for c in chunks[1:]]
        return [first] + rest

    def _build_analytics_lines(self, metrics: dict, lossless: dict | None) -> list[str]:
        keys = [
            'Spectral Spread',
            'Spectral Skewness',
            'Spectral Kurtosis',
            'Spectral Entropy',
            'Spectral Slope',
            'Spectral Decrease',
            'Spectral Contrast',
            'Spectral Bandwidth',
        ]
        lines: list[str] = ["── Spectral Analytics ──"]
        for k in keys:
            if k in metrics:
                lines.extend(self._format_row(k, self._format_value(k, metrics[k]).strip()))
        if lossless:
            lines.append("")
            lines.append("── Lossless Check ──")
            lines.extend(self._format_row("Cutoff", f"{lossless['cutoff_hz']:.0f} Hz"))
            lines.extend(self._format_row("Brick-wall drop", f"{lossless['brickwall_drop_db']:+.2f} dB"))
            lines.extend(self._format_row("Suspect", str(lossless['suspected_format'])))
            lines.extend(self._format_row("Verdict", str(lossless['verdict'])))
            lines.extend(self._format_row("Confidence", f"{lossless['confidence'] * 100:.1f} %"))
        return lines

    def _draw_analytics_panel(self, ax, metrics: dict, lossless: dict | None) -> None:
        lines = self._build_analytics_lines(metrics, lossless)
        text = "\n".join(lines)
        ax.text(
            0.015, 0.985, text,
            transform=ax.transAxes,
            ha='left', va='top',
            family='monospace',
            fontsize=9,
            color=self.colors['text'],
            multialignment='left',
            linespacing=1.25,
            bbox=dict(
                boxstyle='round,pad=0.5',
                facecolor=self.colors['background'],
                edgecolor=self.colors['grid'],
                alpha=0.9,
            ),
        )

    def _draw_cutoff_marker_x(self, ax, lossless: dict | None, fs: int) -> None:
        if not lossless:
            return
        cutoff = float(lossless.get('cutoff_hz', 0.0))
        if cutoff <= 0 or cutoff >= fs / 2:
            return
        ax.axvline(cutoff, color=self.colors['secondary'], linestyle=':', linewidth=2, alpha=0.9)
        ax.text(
            cutoff, 1.005, f"Cutoff {cutoff:.0f} Hz",
            transform=ax.get_xaxis_transform(),
            ha='center', va='bottom',
            fontsize=9, fontweight='bold',
            color=self.colors['secondary'],
            bbox=dict(boxstyle='round,pad=0.2',
                      facecolor=self.colors['background'],
                      edgecolor=self.colors['secondary'],
                      alpha=0.9),
        )

    def create_spectrum_plot(
        self,
        freqs: np.ndarray,
        psd_db: np.ndarray,
        metrics: dict,
        scores: dict,
        total: float,
        filename: str,
        fs: int,
        lossless: dict | None = None,
    ):
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(16, 10),
            constrained_layout=True,
            facecolor=self.colors['background'],
        )

        ax1.semilogx(freqs, psd_db,
                     color=self.colors['accent'],
                     alpha=0.85,
                     linewidth=2,
                     antialiased=True)

        ax1.set_xlabel("Frequency (Hz)", fontsize=12, color=self.colors['text'], fontweight='bold')
        ax1.set_ylabel("Power (dB)", fontsize=12, color=self.colors['text'], fontweight='bold')
        ax1.grid(which='both', linestyle='-', alpha=0.3, color=self.colors['grid'])
        ax1.set_xlim(10, 40000)
        ax1.margins(y=0.2)
        ax1.tick_params(colors=self.colors['text'], labelsize=10)
        for spine in ax1.spines.values():
            spine.set_color(self.colors['grid'])

        for i, (band, (f_low, f_high)) in enumerate(BANDS.items()):
            color_idx = i / len(BANDS)
            band_color = plt.cm.Set3(color_idx)
            ax1.axvspan(f_low, f_high, alpha=0.15, color=band_color)
            ax1.text(
                (f_low + f_high) / 2, -0.15, band,
                transform=ax1.get_xaxis_transform(),
                ha='center', va='top',
                fontsize=11,
                fontweight='bold',
                color=self.colors['text'],
                bbox=dict(boxstyle='round,pad=0.3',
                          facecolor=self.colors['background'],
                          alpha=0.8,
                          edgecolor=self.colors['grid']),
            )

        nyquist = fs / 2
        if nyquist < 40000:
            ax1.axvline(nyquist, color=self.colors['warning'], linestyle='--', alpha=0.8, linewidth=2)
            ax1.text(
                nyquist, -0.15, f'Nyquist ({nyquist:.0f} Hz)',
                transform=ax1.get_xaxis_transform(),
                ha='right', va='top',
                color=self.colors['warning'],
                fontsize=10,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2',
                          facecolor=self.colors['background'],
                          alpha=0.9),
            )

        self._draw_cutoff_marker_x(ax1, lossless, fs)
        self._draw_analytics_panel(ax1, metrics, lossless)

        band_names = list(BANDS.keys())
        extra_names = [k for k in scores.keys() if k not in BANDS]
        all_names = band_names + extra_names
        band_scores = [scores.get(b, 0) for b in all_names]
        colors = plt.cm.viridis(np.linspace(0, 1, len(all_names)))

        bars = ax2.bar(range(len(all_names)), band_scores,
                       color=colors,
                       alpha=0.8,
                       edgecolor=self.colors['background'],
                       linewidth=1)

        ax2.set_title("Band and Metric Scores",
                      pad=15, fontsize=14, fontweight='bold', color=self.colors['text'])
        ax2.set_ylabel("Score / 100", fontsize=12, color=self.colors['text'], fontweight='bold')
        ax2.set_ylim(0, 110)
        ax2.set_xticks(range(len(all_names)))
        ax2.set_xticklabels(all_names, rotation=45, ha='right', fontsize=10, color=self.colors['text'])
        ax2.tick_params(colors=self.colors['text'], labelsize=10)
        ax2.grid(axis='y', alpha=0.3, color=self.colors['grid'])
        for spine in ax2.spines.values():
            spine.set_color(self.colors['grid'])

        for bar, score in zip(bars, band_scores):
            ax2.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                f'{score:.1f}',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold',
                color=self.colors['text'],
            )

        fig.suptitle(f'Spectrum Analysis: {filename}',
                     fontsize=16, fontweight='bold',
                     color=self.colors['text'], y=0.99)

        return fig

    def create_waterfall_plot(
        self,
        data: np.ndarray,
        fs: int,
        metrics: dict,
        filename: str,
        lossless: dict | None = None,
        n_fft: int = 4096,
        overlap: float = 0.75,
    ):
        nperseg = min(n_fft, len(data))
        noverlap = int(nperseg * overlap)
        f, t, sxx = spectrogram(
            data, fs=fs, window='hann',
            nperseg=nperseg, noverlap=noverlap,
            scaling='spectrum', mode='psd',
        )
        sxx_db = 10.0 * np.log10(sxx + 1e-12)

        fig, ax = plt.subplots(
            figsize=(16, 9),
            constrained_layout=True,
            facecolor=self.colors['background'],
        )

        vmax = float(np.percentile(sxx_db, 99))
        vmin = vmax - 80.0
        mesh = ax.pcolormesh(
            t, f, sxx_db,
            shading='auto',
            cmap='magma',
            vmin=vmin, vmax=vmax,
        )
        ax.set_yscale('symlog', linthresh=100)
        ax.set_ylim(20, fs / 2)
        ax.set_xlabel("Time (s)", fontsize=12, color=self.colors['text'], fontweight='bold')
        ax.set_ylabel("Frequency (Hz)", fontsize=12, color=self.colors['text'], fontweight='bold')
        ax.tick_params(colors=self.colors['text'], labelsize=10)
        for spine in ax.spines.values():
            spine.set_color(self.colors['grid'])

        if lossless:
            cutoff = float(lossless.get('cutoff_hz', 0.0))
            if 0 < cutoff < fs / 2:
                ax.axhline(cutoff, color=self.colors['secondary'], linestyle=':', linewidth=2, alpha=0.95)
                ax.text(
                    1.005, cutoff, f"Cutoff {cutoff:.0f} Hz",
                    transform=ax.get_yaxis_transform(),
                    ha='left', va='center',
                    fontsize=9, fontweight='bold',
                    color=self.colors['secondary'],
                    bbox=dict(boxstyle='round,pad=0.2',
                              facecolor=self.colors['background'],
                              edgecolor=self.colors['secondary'],
                              alpha=0.9),
                )

        self._draw_analytics_panel(ax, metrics, lossless)

        cbar = fig.colorbar(mesh, ax=ax, pad=0.02)
        cbar.set_label("Power (dB)", color=self.colors['text'], fontweight='bold')
        cbar.ax.tick_params(colors=self.colors['text'])

        fig.suptitle(f'Spectrogram: {filename}',
                     fontsize=16, fontweight='bold',
                     color=self.colors['text'], y=0.99)

        return fig
