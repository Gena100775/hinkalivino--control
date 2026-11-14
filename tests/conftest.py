import os
import tempfile
from pathlib import Path
import pytest

os.environ.setdefault('DATABASE_URL','sqlite:///'+str(Path(tempfile.mkdtemp())/'test.sqlite3'))
os.environ['HV_ADMIN_PASSWORD']='TestOnlyPassword_2026_ChangeMe'
os.environ['HV_ALLOWED_HOSTS']='testserver,localhost,127.0.0.1'

@pytest.fixture(autouse=True)
def clear_login_throttle():
 from backend.main import failures
 failures.clear()
 yield
 failures.clear()
