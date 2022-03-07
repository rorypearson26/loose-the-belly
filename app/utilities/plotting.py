from lib2to3.pgen2.pgen import DFAState
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from app.utilities.database_utils import retrieve_data_points

output_path = Path(Path(__file__).parent / "plot_output" / "return_plot.jpg")
output_path.parent.mkdir(parents=True, exist_ok=True)


def plot_time_series(length):
    data = retrieve_data_points(length)
    df = process_data(data)
    create_plot(df)
    # msg_block = create_image_block()
    return output_path


def create_plot(df):
    fig, ax = plt.subplots()
    ax.scatter(df.date, df.weight)
    fig.show()
    fig.savefig(output_path)


def create_image_block():
    block = {
        "type": "image",
        "title": {"type": "plain_text", "text": "Please enjoy this photo of a kitten"},
        "block_id": "image4",
        "image_url": f"{output_path}",
        "alt_text": "An incredibly cute kitten.",
    }
    return block


def process_data(data):
    df = pd.DataFrame.from_records([w.to_dict() for w in data])
    df.sort_values(by="date", inplace=True)
    return df


if __name__ == "__main__":
    plot_time_series(6)
    print(output_path)
