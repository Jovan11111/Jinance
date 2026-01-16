import os
import shutil
from datetime import datetime

import matplotlib.pyplot as plt


class GraphBuilder:
    def __init__(self, output_dir="graphs"):
        print("GraphBuilder initialized")
        self.output_dir = output_dir
        self.clear_graph_folder()

    def clear_graph_folder(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def build_price_graph(self, prices: list[float], ticker: str) -> str:
        x = range(len(prices))
        pct_changes = [
            (prices[i] - prices[i - 1]) / prices[i - 1] * 100 if prices[i - 1] else 0.0
            for i in range(1, len(prices))
        ]

        plt.figure(figsize=(8, 4))
        plt.plot(x, prices, marker="o")

        for i, price in enumerate(prices):
            if i == 0:
                continue
            pct = pct_changes[i - 1]
            plt.annotate(
                f"{pct:+.2f}%",
                (i, price),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color="green" if pct > 0 else "red" if pct < 0 else "gray",
            )

        min_p, max_p = min(prices), max(prices)
        margin = (max_p - min_p) * 0.1 or max(1.0, abs(max_p) * 0.01)
        plt.ylim(min_p - margin, max_p + margin)

        plt.xlabel("Dani")
        plt.ylabel("Cena (USD)")
        plt.grid(True)

        path = os.path.join(
            self.output_dir, f"{ticker}_{datetime.now():%Y%m%d_%H%M%S}.png"
        )

        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        return path
