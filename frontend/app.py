import gradio as gr
import os
import requests
import pandas as pd
from pathlib import Path

API_URL = os.environ.get("API_URL", "http://localhost:8000")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "Data_Template.xlsx")

def create_row(anomaly):
    row = {
        "status": anomaly['status'],
        "row_id": anomaly['data']['row_id'] + 1,
        "anomaly_score": anomaly['data']['anomaly_score'],
        "risk_level": anomaly['data']['risk_level'],
    }

    return row


def call_predict(file):
    if Path(file).suffix not in ('.xls', '.xlsx'):
        raise gr.Error('File must be either be in .xls or .xlsx format', duration=5)

    with open(file, 'rb') as f:
        response = requests.post(
            f"API_URL/predict",
            files={"file": f},
            timeout=60
        )

        if response.status_code != 200:
            raise gr.Error(f"Backend error: {response.json()['detail']}")

        print(response.status_code, response.text)

        response = response.json()

    formatted_anomalies = []

    for anomaly in response['anomalies']:
        formatted_row = create_row(anomaly)
        formatted_anomalies.append(formatted_row)

    df = pd.DataFrame(formatted_anomalies, columns=['status', 'row_id', 'anomaly_score', 'risk_level'])

    return df


with gr.Blocks() as app:
    gr.Markdown("# Use the template to enter data, then submit to detect anomalies.")
    with gr.Column():
        with gr.Row():
            data_inp = gr.File()
            gr.DownloadButton(
                label="Download Template",
                value=TEMPLATE_PATH
            )
        with gr.Row():
            submit_btn = gr.Button("Submit")

        with gr.Row():
            output_data = gr.DataFrame()

    # Submit Call
    submit_btn.click(
        fn=call_predict,
        inputs=data_inp,
        outputs=output_data
    )

app.launch()