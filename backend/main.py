from fastapi import FastAPI, UploadFile, HTTPException
from io import BytesIO

from preprocessing import load_predict_data
from exceptions import InvalidFileTypeError, OmittedColumnsError
from model import predict
from schema import create_json_res

app = FastAPI()

@app.post("/predict")
async def predict_anomalies(file: UploadFile):
    try:
        data = await file.read()
        df = load_predict_data(BytesIO(data))

    except InvalidFileTypeError as e:
        raise HTTPException(
            status_code= 415,
            detail= str(e)
        )

    except OmittedColumnsError as e:
        raise HTTPException(
            status_code= 400,
            detail= str(e)
        )

    df = predict(df)

    anomalies = []
    for index, row in df.iterrows():
        if row['anomaly'] < 0.0:
            anomalies.append(create_json_res(index, row))

    return {"status": "ok", "anomalies": anomalies}