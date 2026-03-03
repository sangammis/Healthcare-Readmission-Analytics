import pandas as pd
import numpy as np
import os
import logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# data path
raw_dir = os.path.join(base_dir, 'data', 'raw')
os.makedirs(raw_dir, exist_ok = True)
raw_path = os.path.join(raw_dir, "diabetes_130_raw.csv")

processed_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(processed_dir, exist_ok = True)
processed_path = os.path.join(processed_dir, "processed_diabetes_130.csv")

log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok = True)

log_file = os.path.join(log_dir, "pipeline.log")

# logging

logging.basicConfig(
    filename = log_file,
    level = logging.INFO,
    format = "%(asctime)s : %(levelname)s : %(message)s"
)

# load data
def load_data(path):
    try:
        df = pd.read_csv(path)
        logging.info("Data loaded successfully")
        return df
    except Exception as e:
        logging.error(f"Error loading data : {e}")
        raise

# clean data
def clean_data(df):
    df.replace("?", np.nan, inplace = True)
    df = df.ffill()
    logging.info("Data Cleaned")
    return df

# save data
def save_processed_data(df, path):
    df.to_csv(path, index = False)
    logging.info("Processed data saved")

# main
def main():
    logging.info("Healthcare pipeline started")

    df = load_data(raw_path)
    df = clean_data(df)

    save_processed_data(df, processed_path)

    logging.info("Healthcare pipeline completed")

if __name__ == "__main__":
    main()