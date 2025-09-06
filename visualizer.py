import matplotlib.pyplot as plt
import numpy as np
from constants import BANDS
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors

class AudioVisualizer:
    def __init__(self, theme='dark'):
        self.theme = theme
        self._setup_theme()

    def _setup_theme(self):
        if self.theme == 'light':
            plt.style.use('default')
            self.colors = {
                'background': '#FFFFFF',
                'grid': '#E0E0E0',
                'text': '#212121',
                'accent': '#2196F3',
                'secondary': '#4CAF50',
                'warning': '#FF9800'
            }
        elif self.theme == 'high_contrast':
            plt.style.use('default')
            self.colors = {
                'background': '#FFFFFF',
                'grid': '#CCCCCC',
                'text': '#000000',
                'accent': '#1976D2',
                'secondary': '#388E3C',
                'warning': '#D32F2F'
            }
        else:
            plt.style.use('dark_background')
            self.colors = {
                'background': '#000000',
                'grid': '#444444',
                'text': '#FFFFFF',
                'accent': '#4FC3F7',
                'secondary': '#81C784',
                'warning': '#FF8A65'
            }
    def create_spectrum_plot(self, freqs, psd_db, metrics, scores, total, filename, fs):
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(16, 10),
            constrained_layout=True,
            facecolor=self.colors['background']
        )

        line = ax1.semilogx(freqs, psd_db,
                           color=self.colors['accent'],
                           alpha=0.8,
                           linewidth=2,
                           antialiased=True)

        ax1.set_xlabel("Frequency (Hz)",
                      fontsize=12,
                      color=self.colors['text'],
                      fontweight='bold')
        ax1.set_ylabel("Power (dB)",
                      fontsize=12,
                      color=self.colors['text'],
                      fontweight='bold')

        ax1.grid(which='both',
                linestyle='-',
                alpha=0.3,
                color=self.colors['grid'])
        ax1.set_xlim(10, 40000)
        ax1.margins(y=0.2)

        ax1.tick_params(colors=self.colors['text'], labelsize=10)
        for spine in ax1.spines.values():
            spine.set_color(self.colors['grid'])

        for i, (band, (f_low, f_high)) in enumerate(BANDS.items()):
            color_idx = i / len(BANDS)
            band_color = plt.cm.Set3(color_idx)

            ax1.axvspan(f_low, f_high, alpha=0.15, color=band_color)
            # Перемещаем текст в нижнюю часть графика
            ax1.text(
                (f_low + f_high) / 2, -0.15, band,  # Изменили y-координату на отрицательную
                transform=ax1.get_xaxis_transform(),
                ha='center', va='top',  # Изменили выравнивание по вертикали на 'top'
                fontsize=11,
                fontweight='bold',
                rotation=0,
                color=self.colors['text'],
                bbox=dict(boxstyle='round,pad=0.3',
                         facecolor=self.colors['background'],
                         alpha=0.8,
                         edgecolor=self.colors['grid'])
            )

        nyquist = fs / 2
        if nyquist < 40000:
            ax1.axvline(nyquist,
                       color=self.colors['warning'],
                       linestyle='--',
                       alpha=0.8,
                       linewidth=2)
            ax1.text(
                nyquist, -0.15, f'Nyquist ({nyquist:.0f} Hz)',
                transform=ax1.get_xaxis_transform(),
                ha='right', va='top',
                color=self.colors['warning'],
                fontsize=10,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2',
                         facecolor=self.colors['background'],
                         alpha=0.9)
            )

        band_names = list(BANDS.keys()) + ['flatness', 'centroid']
        band_scores = [scores.get(b, 0) for b in band_names]
        colors = plt.cm.viridis(np.linspace(0, 1, len(band_names)))

        bars = ax2.bar(range(len(band_names)), band_scores,
                      color=colors,
                      alpha=0.8,
                      edgecolor=self.colors['background'],
                      linewidth=1)

        ax2.set_title("Band and Metric Scores",
                     pad=15,
                     fontsize=14,
                     fontweight='bold',
                     color=self.colors['text'])
        ax2.set_ylabel("Score / 100",
                      fontsize=12,
                      color=self.colors['text'],
                      fontweight='bold')
        ax2.set_ylim(0, 110)
        ax2.set_xticks(range(len(band_names)))
        ax2.set_xticklabels(band_names,
                           rotation=45,
                           ha='right',
                           fontsize=11,
                           color=self.colors['text'])

        ax2.tick_params(colors=self.colors['text'], labelsize=10)
        ax2.grid(axis='y', alpha=0.3, color=self.colors['grid'])
        for spine in ax2.spines.values():
            spine.set_color(self.colors['grid'])

        for bar, score in zip(bars, band_scores):
            ax2.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                f'{score:.1f}',
                ha='center',
                va='bottom',
                fontsize=9,
                fontweight='bold',
                color=self.colors['text']
            )

        fig.suptitle(f'Spectrum Analysis: {filename}',
                    fontsize=16,
                    fontweight='bold',
                    color=self.colors['text'],
                    y=0.98)

        return fig
