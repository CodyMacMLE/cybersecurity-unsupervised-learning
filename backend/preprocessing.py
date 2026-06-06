import pandas as pd
from pathlib import Path

from exceptions import InvalidFileTypeError, OmittedColumnsError

COLUMNS = ['duration'
,'protocol_type'
,'service'
,'flag'
,'src_bytes'
,'dst_bytes'
,'land'
,'wrong_fragment'
,'urgent'
,'hot'
,'num_failed_logins'
,'logged_in'
,'num_compromised'
,'root_shell'
,'su_attempted'
,'num_root'
,'num_file_creations'
,'num_shells'
,'num_access_files'
,'num_outbound_cmds'
,'is_host_login'
,'is_guest_login'
,'count'
,'srv_count'
,'serror_rate'
,'srv_serror_rate'
,'rerror_rate'
,'srv_rerror_rate'
,'same_srv_rate'
,'diff_srv_rate'
,'srv_diff_host_rate'
,'dst_host_count'
,'dst_host_srv_count'
,'dst_host_same_srv_rate'
,'dst_host_diff_srv_rate'
,'dst_host_same_src_port_rate'
,'dst_host_srv_diff_host_rate'
,'dst_host_serror_rate'
,'dst_host_srv_serror_rate'
,'dst_host_rerror_rate'
,'dst_host_srv_rerror_rate'
,'attack'
,'level']
FEATURE_COLUMNS = [c for c in COLUMNS if c not in ('attack', 'level')]

def load_training_data(filepath: str) -> pd.DataFrame:
    file_path = Path(filepath)
    # LOAD FROM FILE
    if file_path.suffix == ".csv":
        df = pd.read_csv(filepath, header=None, names=COLUMNS)
    else:
        raise InvalidFileTypeError(f"Invalid file type: Expected '.csv', got '{Path(file_path).suffix}'")

    # ONLY KEEP NORMAL DATA CALLS - REMOVE ATTACKS
    df = df[df['attack'] == 'normal']
    # DROP LABELS
    df = df.drop(columns=['attack', 'level'])
    return df

def load_predict_data(file) -> pd.DataFrame:
    # LOAD FROM FILE
    df = pd.read_excel(file, sheet_name=0, header=0)

    omitted_cols = set(FEATURE_COLUMNS).difference(set(df.columns))

    if omitted_cols:
        raise OmittedColumnsError(f"Omitted Columns: Expects '{omitted_cols}'")

    return df