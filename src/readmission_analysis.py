import pandas as pd
import numpy as np
import os
import logging

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

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
    df = df.fillna("Unknown")
    logging.info("Data Cleaned")
    return df

# Feature Engineering
def feature_engineering(df, is_train = True, encoders = None):
    """
    Standardizes feature encoding to avoid data leakage.
    """
    df = df.copy() # Avoid SettingWithCopyWarning
    
    if encoders is None:
        encoders = {}
    
    cat_cols = df.select_dtypes(include = ['object', 'category']).columns

    for col in cat_cols:
        if is_train:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        else:
            le = encoders.get(col)
            if le is None:
                continue
            # Handle unseen labels in test set by mapping to the first known class
            df[col] = df[col].astype(str).map(lambda s: s if s in le.classes_ else le.classes_[0])
            df[col] = le.transform(df[col])
            
    logging.info(f"Feature Engineering: Encoded {len(cat_cols)} categorical columns.")
    return df, encoders
# Train Model
def train_models(X_train, y_train, X_test, y_test):

    # Logistic Regression
    lr = LogisticRegression(max_iter=2000)
    lr.fit(X_train,y_train)
    pred_lr = lr.predict(X_test)
    
    logging.info(f"LR Accuracy: {accuracy_score(y_test, pred_lr)}")

    #XGBoost
    xgb = XGBClassifier(eval_metric = 'logloss')
    xgb.fit(X_train, y_train)
    pred_xgb = xgb.predict(X_test)

    logging.info(f"XGB Accuracy : {accuracy_score(y_test, pred_xgb)}")

    return lr, xgb



# save data
def save_processed_data(df, path):
    df.to_csv(path, index = False)
    logging.info("Processed data saved")

# main
def main():
    logging.info("Healthcare pipeline started")

    df = load_data(raw_path)
    df = clean_data(df)

    # Encoded target first

    df['readmitted'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)

    save_processed_data(df, processed_path)

    # Split BEFORE encoding to prevent leakage
    X = df.drop("readmitted", axis = 1)
    y = df["readmitted"]
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size = 0.2, random_state = 42
    )

   # Encode Train and Test separately
    X_train, encoders = feature_engineering(X_train_raw, is_train=True)
    X_test, _ = feature_engineering(X_test_raw, is_train=False, encoders=encoders)

    # Train and Evaluate
    lr_model, xgb_model = train_models(X_train, y_train, X_test, y_test)

    logging.info("Healthcare pipeline completed")

if __name__ == "__main__":
    main()