from fastapi.testclient import TestClient
from backend.main import app
import os


def login(c,name,password):
 r=c.post('/api/login',json={'username':name,'password':password})
 assert r.status_code==200,r.text
 return {'Authorization':'Bearer '+r.json()['token']}


def test_all_roles_and_server_permissions():
 with TestClient(app) as c:
  owner=login(c,'owner',os.environ['HV_ADMIN_PASSWORD'])
  for role in ['manager','chef','accountant','souschef','bar','buyer']:
   name='matrix_'+role
   password='SyntheticRoleMatrixPassword_2026'
   r=c.post('/api/users',headers=owner,json={'username':name,'password':password,'role':role,'site':'my'})
   assert r.status_code==200,r.text
   h=login(c,name,password)
   assert c.get('/api/me',headers=h).json()['role']==role
   assert c.get('/api/users',headers=h).status_code==403
   assert c.get('/api/orders',headers=h).status_code==200
   assert c.get('/api/audit',headers=h).status_code==(200 if role in ['manager','accountant'] else 403)
   cross=c.get('/api/stock/neg',headers=h)
   assert cross.status_code==(403 if role in ['souschef','bar'] else 200)
   r=c.post('/api/orders',headers=h,json={'site':'my','product_id':1,'qty':1,'unit_price':100})
   assert r.status_code==(403 if role in ['bar','accountant'] else 200)
  assert c.get('/api/stock/unknown',headers=owner).status_code==400


def test_login_sql_injection_validation_and_browser_policy():
 with TestClient(app) as c:
  assert c.post('/api/login',json={'username':"owner' OR 1=1 --",'password':'wrong'}).status_code==401
  secret='synthetic-sensitive-input'
  r=c.post('/api/users',headers=login(c,'owner',os.environ['HV_ADMIN_PASSWORD']),json={'username':'xx','password':secret,'role':'owner'})
  assert r.status_code==422
  assert secret not in r.text
  r=c.get('/')
  assert "script-src 'self';" in r.headers['content-security-policy']
  assert '<script>' not in r.text
  assert c.get('/assets/app.js').status_code==200
  assert c.get('/assets/styles.css').status_code==200
  assert c.get('/assets/../../backend/main.py').status_code==404


def test_buyer_cannot_receive_goods():
 with TestClient(app) as c:
  owner=login(c,'owner',os.environ['HV_ADMIN_PASSWORD'])
  password='SyntheticBuyerOnlyPassword_2026'
  assert c.post('/api/users',headers=owner,json={'username':'receipt_buyer','password':password,'role':'buyer'}).status_code==200
  buyer=login(c,'receipt_buyer',password)
  oid=c.post('/api/orders',headers=buyer,json={'site':'tag','product_id':2,'qty':2,'unit_price':123}).json()['id']
  assert c.post(f'/api/orders/{oid}/advance',headers=buyer).json()['status']=='sent'
  assert c.post(f'/api/orders/{oid}/advance',headers=buyer).json()['status']=='delivered'
  assert c.post(f'/api/orders/{oid}/advance',headers=buyer).status_code==403
  assert c.post(f'/api/orders/{oid}/advance',headers=owner).json()['status']=='received'
  assert c.post(f'/api/orders/{oid}/advance',headers=owner).status_code==409


def test_parallel_receipt_credits_stock_once():
 from concurrent.futures import ThreadPoolExecutor
 import pytest
 from backend.main import URL
 if URL.startswith('sqlite'):pytest.skip('Row-lock concurrency requires PostgreSQL')
 with TestClient(app) as c:
  owner=login(c,'owner',os.environ['HV_ADMIN_PASSWORD'])
  before=next(x['qty'] for x in c.get('/api/stock/neg',headers=owner).json() if x['id']==3)
  oid=c.post('/api/orders',headers=owner,json={'site':'neg','product_id':3,'qty':7,'unit_price':99}).json()['id']
  for _ in range(2):assert c.post(f'/api/orders/{oid}/advance',headers=owner).status_code==200
  with ThreadPoolExecutor(max_workers=2) as pool:
   statuses=list(pool.map(lambda _:c.post(f'/api/orders/{oid}/advance',headers=owner).status_code,range(2)))
  assert sorted(statuses)==[200,409]
  after=next(x['qty'] for x in c.get('/api/stock/neg',headers=owner).json() if x['id']==3)
  assert float(after)-float(before)==7
