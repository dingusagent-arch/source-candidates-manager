from pathlib import Path
import pytest

@\pytest.fixture
def sample_csv_path():
    # locate sample CSV relative to this file's package
    base = Path(__file__).resolve().parent.parent / 'src' / 'importers' / 'examples'
    return base / 'opportunities.csv'
