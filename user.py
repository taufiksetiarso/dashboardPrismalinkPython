import logging
import os
from flaskr.db_postgresql import get_db
from flask import (
    Blueprint,
    Response,
    request
)
import json
from pprint import pprint
import datetime
import redis
logging.basicConfig(format='%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

bp = Blueprint("user", __name__, url_prefix="/user")
r = redis.Redis(
    host='localhost',
    port=6379  , 
    password='')

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
@bp.route("/login", methods = ['POST'])
def login():
    db = get_db()
    cur = db.cursor()
    logging.debug(request.get_json())
    data=request.get_json()
    email=data['email']
    password=data['password']
    logging.debug(email,"asd ",email,password)
    try:
        postgreSQL_select_Query = "SELECT * from mbdd_user where mbdd_user_email=%s and mbdd_user_password=%s"

        cur.execute(postgreSQL_select_Query, (email,password,))
      
            
    except:
        logging.debug("I can't SELECT from mdo_merchant_limit")
    row = cur.fetchone()
    cur.close()
    if not bool(row):
        return Response(json.dumps({'responseCode': 'MBDD01', 'responseMessage': 'INVALID_PARAMETER', 'responseDescription': 'query result is empty'}), mimetype='application/json')
    columns = (
        'userId',
        'userPassword',
        'userRole',
        'userFullname',
        'balance',
        'isLogin',
        'email',
        'mobile',
        'merchantCode',
        'merchantId'
    )
    data = dict(zip(columns, row))
    r = {
        'responseCode': 'MBDD00',
        'responseMessage': 'SUCCESS',
        'responseDescription': 'SUCCESS',
        'user': data,
        'sessionToken':'token'
    }
    y = json.dumps(r, indent=2, default=default)
    return Response(y, mimetype='application/json')