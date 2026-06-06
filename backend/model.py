import joblib
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline

MODEL_PATH = Path(__file__).parent / "models" / "security_model.joblib"

def train(df: pd.DataFrame) -> None:
    """
    Builds and trains a pipeline with ColumnTransformer
    to handle categorical features and IsolationForest.
    """

    # 1. Define categorical columns that need encoding
    categorical_features = ['protocol_type', 'service', 'flag']

    # 2. Create the ColumnTransformer
    # 'passthrough' keeps your numerical columns as-is
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat_labels', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )

    # 3. Create the full Pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', IsolationForest(contamination=0.01, random_state=42))
    ])

    # 4. Train the pipeline
    # Note: 'df' should already be cleaned by preprocessing.py
    pipeline.fit(df)

    # 5. Save the entire bundle
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print("Pipeline trained and saved successfully.")

def get_risk_level(score: float) -> str:
    if score < -0.8:
        return "Critical"
    elif score < -0.1:
        return "Medium"
    else:
        return "Low"

def predict(df: pd.DataFrame) -> pd.DataFrame:
    # load model from disk
    pipeline = joblib.load(MODEL_PATH)

    # pass through data for predictions
    df['anomaly'] = pipeline.decision_function(df)

    df['risk_level'] = df.apply(lambda row: get_risk_level(row['anomaly']) if row['anomaly'] < 0.0 else 'None', axis=1)

    # return dataframe with anomaly scores added
    return df