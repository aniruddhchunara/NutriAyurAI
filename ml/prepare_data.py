import pandas as pd

from analytics.data_loader import load_data




def prepare_dataset():

    df = load_data()

    print(df.head())













if __name__ == "__main__":
    prepare_dataset()