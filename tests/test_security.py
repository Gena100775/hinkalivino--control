from fastapi.testclient import TestClient
from backend.main import app
from test_smoke import os

def test_employee_lifecycle_and_task_permissions():
 with TestClient(app) as c:
  def login(name,password):
   r=c.post('/api/login',json={'username':name,'password':password})
   assert r.status_code==200,r.text
   return {'Authorization':'Bearer '+r.json()['token']}
  owner=login('owner',os.environ['HV_ADMIN_PASSWORD'])
  password='SyntheticEmployeePassword_2026'
  for name,role in [('test_bar','bar'),('test_sous','souschef')]:
   assert c.post('/api/users',headers=owner,json={'username':name,'password':password,'role':role,'site':'neg'}).status_code==200
  bar=login('test_bar',password)
  sous=login('test_sous',password)
  assert c.get('/api/users',headers=bar).status_code==403
  assert c.get('/api/stock/my',headers=bar).status_code==403
  task=c.post('/api/tasks',headers=owner,json={'site':'neg','title':'Synthetic test task','assignee_role':'souschef'}).json()['id']
  assert c.post(f'/api/tasks/{task}/toggle',headers=bar).status_code==403
  assert c.post(f'/api/tasks/{task}/toggle',headers=sous).status_code==200
  accounts=c.get('/api/users',headers=owner).json()
  assert all('passhash' not in x for x in accounts)
  bar_id=next(x['id'] for x in accounts if x['username']=='test_bar')
  assert c.post(f'/api/users/{bar_id}/active',headers=owner,json={'active':False}).status_code==200
  assert c.get('/api/me',headers=bar).status_code==401
  assert c.post('/api/login',json={'username':'test_bar','password':password}).status_code==401
  assert c.post('/api/me/password',headers=sous,json={'current_password':'wrong','new_password':'ChangedSyntheticPassword_2026'}).status_code==400
  assert c.post('/api/me/password',headers=sous,json={'current_password':password,'new_password':'ChangedSyntheticPassword_2026'}).status_code==200
  assert c.get('/api/me',headers=sous).status_code==401
  login('test_sous','ChangedSyntheticPassword_2026')

def test_host_headers_and_login_throttle():
 with TestClient(app) as c:
  assert c.get('/',headers={'Host':'attacker.invalid'}).status_code==400
  r=c.get('/')
  assert r.headers['cache-control']=='no-store'
  assert r.headers['x-frame-options']=='DENY'
  for _ in range(8):
   assert c.post('/api/login',json={'username':'nonexistent','password':'wrong'}).status_code==401
  assert c.post('/api/login',json={'username':'nonexistent','password':'wrong'}).status_code==429
