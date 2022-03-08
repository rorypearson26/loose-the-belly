from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

from app.utilities.database_utils import retrieve_data_points

output_path = Path(Path(__file__).parent / "plot_output" / "return_plot.jpg")
output_path.parent.mkdir(parents=True, exist_ok=True)


def plot_time_series(length):
    data = retrieve_data_points(length)
    df = process_data(data)
    create_plot(df)
    return output_path


def create_plot(df):
    fig, ax = plt.subplots()
    colours = ['r', 'b', 'g']
    i = 0
    for key, grp in df.groupby(['clothing_code']):
        x = mdates.date2num(grp['date'])
        z = np.polyfit(x, grp['weight'], 1)
        p = np.poly1d(z)
        ax.plot(x,p(x),f"{colours[i]}--")
        ax.scatter(grp['date'], grp['weight'], c=colours[i], label=key)
        i += 1
        # Setup nice date format.
        locator = mdates.MonthLocator()  # every month
        fmt = mdates.DateFormatter('%b')
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        # Specify formatter
        X.set_major_formatter(fmt)
        plt.grid(visible=True, which='both')
        ax.legend()
        fig.savefig(output_path)


def process_data(data):
    df = pd.DataFrame.from_records([w.to_dict() for w in data])
    df.sort_values(by="date", inplace=True)
    return df
