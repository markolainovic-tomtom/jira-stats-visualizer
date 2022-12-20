import matplotlib.pyplot as plt
from typing import List, Optional
import pandas as pd


class BoxPlotter:
    def __init__(self, values: List[int]) -> None:
        self.df = pd.DataFrame(values)

    def plot(self, title: str, ylabel: str, ylims: Optional[List[int]] = None):
        plt.figure()
        self.df.boxplot(xlabel=f"Sample size: {len(self.df)}", ylabel=ylabel)
        plt.show(block=False)
        fig = plt.gcf()
        fig.suptitle(title)
        fig.canvas.manager.set_window_title(title)
        if ylims:
            plt.ylim(bottom=ylims[0], top=ylims[1])
        fig.savefig(title)
