import os
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# Path for saving preprocessing objects and model
# Get the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate to the parent folder and then to the PreProcessors folder
PREPROCESS_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "../PreProcessors2"))
os.makedirs(PREPROCESS_PATH, exist_ok=True)

# Features
CATEGORICAL_FEATURES = [
    "released", "writer", "rating", "name", "genre",
    "director", "star", "country", "company"
]
NUMERICAL_FEATURES = [
    "runtime", "score", "year", "votes", "log_budget",
    "budget_vote_ratio", "budget_runtime_ratio", "budget_score_ratio",
    "vote_score_ratio", "budget_year_ratio", "vote_year_ratio",
    "score_runtime_ratio", "budget_per_minute", "votes_per_year",
    "is_recent", "is_high_budget", "is_high_votes", "is_high_score"
]

def preprocess_data(df, save_objects=False):
    df = df.copy()

    # Log Transformation
    if "gross" in df.columns:
        df["log_gross"] = np.log1p(df["gross"])
    df["log_budget"] = np.log1p(df["budget"])

    # Feature Engineering
    df["budget_vote_ratio"] = df["budget"] / (df["votes"] + 1)
    df["budget_runtime_ratio"] = df["budget"] / (df["runtime"] + 1)
    df["budget_score_ratio"] = df["log_budget"] / (df["score"] + 1)
    df["vote_score_ratio"] = df["votes"] / (df["score"] + 1)
    df["budget_year_ratio"] = df["log_budget"] / (df["year"] - df["year"].min() + 1)
    df["vote_year_ratio"] = df["votes"] / (df["year"] - df["year"].min() + 1)
    df["score_runtime_ratio"] = df["score"] / (df["runtime"] + 1)
    df["budget_per_minute"] = df["budget"] / (df["runtime"] + 1)
    df["votes_per_year"] = df["votes"] / (df["year"] - df["year"].min() + 1)
    df["is_recent"] = (df["year"] >= df["year"].quantile(0.75)).astype(int)
    df["is_high_budget"] = (df["log_budget"] >= df["log_budget"].quantile(0.75)).astype(int)
    df["is_high_votes"] = (df["votes"] >= df["votes"].quantile(0.75)).astype(int)
    df["is_high_score"] = (df["score"] >= df["score"].quantile(0.75)).astype(int)

    # Label Encoding
    for feature in CATEGORICAL_FEATURES:
        df[feature] = df[feature].astype(str)
        le = LabelEncoder()
        if save_objects:
            df[feature] = le.fit_transform(df[feature])
            joblib.dump(le, os.path.join(PREPROCESS_PATH, f"{feature}_encoder.pkl"))
        else:
            try:
                le = joblib.load(os.path.join(PREPROCESS_PATH, f"{feature}_encoder.pkl"))
                df[feature] = le.transform(df[feature])
            except ValueError:
                # Handle unseen labels by assigning a default category
                df[feature] = df[feature].apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )

    # Imputation and Scaling
    imputer = SimpleImputer(strategy="median")
    if save_objects:
        df[NUMERICAL_FEATURES] = imputer.fit_transform(df[NUMERICAL_FEATURES])
        joblib.dump(imputer, os.path.join(PREPROCESS_PATH, "imputer.pkl"))
    else:
        imputer = joblib.load(os.path.join(PREPROCESS_PATH, "imputer.pkl"))
        df[NUMERICAL_FEATURES] = imputer.transform(df[NUMERICAL_FEATURES])

    scaler = StandardScaler()
    if save_objects:
        df[NUMERICAL_FEATURES] = scaler.fit_transform(df[NUMERICAL_FEATURES])
        joblib.dump(scaler, os.path.join(PREPROCESS_PATH, "scaler.pkl"))
    else:
        scaler = joblib.load(os.path.join(PREPROCESS_PATH, "scaler.pkl"))
        df[NUMERICAL_FEATURES] = scaler.transform(df[NUMERICAL_FEATURES])

    # Drop unnecessary columns
    if "gross" in df.columns:
        df = df.drop(["gross", "budget"], axis=1)
    else:
        df = df.drop(["budget"], axis=1)

    return df

def prepare_features(df):
    processed_df = preprocess_data(df, save_objects=True)

    if "log_gross" in processed_df.columns:
        y = processed_df["log_gross"]  # Target
        X = processed_df.drop("log_gross", axis=1)  # Features
    else:
        y = None
        X = processed_df

    return X, y
