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


def test_managed_schema_startup_never_creates_tables(monkeypatch):
 from fastapi.testclient import TestClient
 from sqlalchemy import event
 with TestClient(main.app):
  monkeypatch.setenv('HV_SCHEMA_MANAGED','true')
  statements=[]
  def observe(conn,cursor,statement,parameters,context,executemany):
   statements.append(statement)
  event.listen(main.engine,'before_cursor_execute',observe)
  try:main.initialize()
  finally:event.remove(main.engine,'before_cursor_execute',observe)
  assert statements
  assert not any(q.lstrip().upper().startswith('CREATE ') for q in statements)
