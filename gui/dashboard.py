import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class CyberChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create 2 subplots (1 row, 2 columns)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
        self.fig.patch.set_facecolor('#1A1A1A')
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#1A1A1A')
            ax.tick_params(colors='#00FF41', labelsize=8)
            for spine in ax.spines.values():
                spine.set_edgecolor('#333333')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_chart(self, full_df, anomalies_df):
        """Updates with detailed time and length data."""
        self.ax1.clear()
        self.ax2.clear()
        
        if not full_df.empty:
            # Graph 1: Response Length Distribution (Scatter)
            self.ax1.scatter(full_df.index, full_df['response_len'], color="#08F51C", alpha=0.5, label='Normal')
            if not anomalies_df.empty:
                # Highlight the "weird" anomalies in Red
                self.ax1.scatter(anomalies_df.index, anomalies_df['response_len'], color='#FF3131', label='Anomaly')
            self.ax1.set_title("Response Size Variance (Z-Score)", color='#00FF41', fontsize=10)
            self.ax1.legend(facecolor='#1A1A1A', labelcolor='white', fontsize=7)

            # Graph 2: Response Latency (Time-Based)
            self.ax2.plot(full_df.index, full_df['response_time'], color='#00FF41', linewidth=1)
            self.ax2.set_title("Response Latency (Seconds)", color='#00FF41', fontsize=10)
            self.ax2.set_ylabel("Seconds", color='#00FF41', fontsize=8)

        self.fig.tight_layout()
        self.canvas.draw()