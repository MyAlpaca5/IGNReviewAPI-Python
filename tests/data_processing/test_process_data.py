import os
import pandas as pd

from app.data_processing.process_data import process_raw


def test_process_raw():
    file_path_root = os.path.dirname(__file__)

    raw = pd.read_csv(
        os.path.join(file_path_root, "data/raw.csv"),
        encoding="utf8",
        na_values=" "
    )
    actual, _ = process_raw(raw)
    expected = pd.read_csv(
        os.path.join(file_path_root, "data/processed.csv"),
        encoding="utf-8",
        na_values=" ",
    )

    # Nan value in pandas is not equal, nan != nan,
    # so convert them to empty string for comparison
    actual = actual.fillna("")
    expected = expected.fillna("")

    assert actual.equals(expected)
