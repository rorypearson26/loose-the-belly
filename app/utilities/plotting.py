import matplotlib.pyplot as plt
import pandas as pd

from app.utilities.database_utils import retrieve_data_points

def plot_time_series(length):
    data = retrieve_data_points(length)
    df = pd.DataFrame.from_records([w.to_dict() for w in data])
    print(df)