import os,tempfile
from pathlib import Path
from fastapi.testclient import TestClient
p=Path(tempfile.mkdtemp())/'test.sqlite3'
os.environ.setdefault('DATABASE_URL','sqlite:///'+str(p))
os.environ['HV_ADMIN_PASSWORD']='TestOnlyPassword_2026_ChangeMe'
os.environ['HV_ALLOWED_HOSTS']='testserver,localhost,127.0.0.1'
from backend.main import app

def test_auth_orders_inventory_and_scoping():
 with TestClient(app) as c:
  assert c.get('/api/health').status_code==200
  assert c.get('/api/orders').status_code==401
  login=c.post('/api/login',json={'username':'owner','password':os.environ['HV_ADMIN_PASSWORD']})
  assert login.status_code==200,login.text
  h={'Authorization':'Bearer '+login.json()['token']}
  created=c.post('/api/users',headers=h,json={'username':'sous','password':'AnotherSecurePassword_2026','role':'souschef','site':'my'})
  assert created.status_code==200,created.text
  sh={'Authorization':'Bearer '+c.post('/api/login',json={'username':'sous','password':'AnotherSecurePassword_2026'}).json()['token']}
  assert c.get('/api/stock/tag',headers=sh).status_code==403
  assert c.post('/api/users',headers=sh,json={'username':'test','password':'AnotherSecurePassword_2026','role':'owner'}).status_code==403
  order=c.post('/api/orders',headers=sh,json={'site':'my','product_id':1,'qty':25,'unit_price':850})
  assert order.status_code==200,order.text
  oid=order.json()['id']
  for expected in ['sent','delivered','received']:
   response=c.post(f'/api/orders/{oid}/advance',headers=sh)
   assert response.status_code==200,response.text
   assert response.json()['status']==expected
  assert c.post(f'/api/orders/{oid}/advance',headers=sh).status_code==409
  stock=c.get('/api/stock/my',headers=h).json()
  assert float(next(x['qty'] for x in stock if x['id']==1))==25
  inv=c.post('/api/inventory',headers=sh,json={'site':'my','product_id':1,'counted':22})
  assert inv.status_code==200 and inv.json()['difference']==-3
  assert c.get('/api/audit',headers=sh).status_code==403
  assert c.post('/api/logout',headers=sh).status_code==200
  assert c.get('/api/me',headers=sh).status_code==401
