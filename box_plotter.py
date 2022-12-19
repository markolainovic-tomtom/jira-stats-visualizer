import matplotlib.pyplot as plt
from typing import List
import pandas as pd

# import matplotlib
# matplotlib.use('Agg')


class BoxPlotter:
    def __init__(self, values: List[int]) -> None:
        self.df = pd.DataFrame(values)

    def plot(self, title: str):
        plt.figure()
        self.df.boxplot(xlabel=f"Sample size: {len(self.df)}")
        plt.show(block=False)
        fig = plt.gcf()
        fig.suptitle(title)
        fig.canvas.manager.set_window_title(title)
        fig.savefig(title)
