import pytest
from backend import main


def test_release_gate_blocks_before_database_access(monkeypatch):
 monkeypatch.setenv('HV_ENV','production')
 monkeypatch.setenv('HV_RELEASE_APPROVED','false')
 def forbidden_connection():
  raise AssertionError('Database must not be accessed before approval')
 monkeypatch.setattr(main.engine,'begin',forbidden_connection)
 with pytest.raises(RuntimeError,match='security release approval required'):
  main.initialize()


def test_render_hostname_is_exact_and_explicit_hosts_take_precedence(monkeypatch):
 monkeypatch.delenv('HV_ALLOWED_HOSTS',raising=False)
 monkeypatch.setenv('RENDER_EXTERNAL_HOSTNAME','hinkalivino--control.onrender.com')
 assert main.configured_hosts()==['hinkalivino--control.onrender.com','localhost','127.0.0.1']
 monkeypatch.setenv('RENDER_EXTERNAL_HOSTNAME','*.onrender.com')
 with pytest.raises(RuntimeError,match='Invalid Render hostname'):
  main.configured_hosts()
 monkeypatch.setenv('HV_ALLOWED_HOSTS','example.test, localhost')
 assert main.configured_hosts()==['example.test','localhost']
