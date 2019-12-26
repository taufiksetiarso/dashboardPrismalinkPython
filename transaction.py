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

logging.basicConfig(format='%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
# logging.warning('Admin logged out')

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
# create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger = logging.getLogger(__name__)


bp = Blueprint("transaction", __name__, url_prefix="/transaction")
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
@bp.route("/detail")
def fetch_all():
    logging.debug("I can'sasaa")
    print("coba dulu ni")
    id = request.args.get('id')
    db = get_db()
    cur = db.cursor()
    # id = '4028811b6d3cabd5016d3cad47e'
    # user_id = '4028d86c6d386583016d3865bc'
    try:
        cur.execute("""
            SELECT id, merc_nm, version, ecomm_ref_no, merc_id, merc_cd, cons_username_merchant, co_ccy_amt, created_dt, issuer_code, merc_ref_no, pay_sts, pay_bnk_ref_no from ecom_ecomm_latest_actv_log where id='%s'
            """ % (id))
    except:
        logging.debug("I can't SELECT from ecom_ecomm_latest_actv_log")
    rows = cur.fetchone()
    columns = ('id', 'mercNm', 'version', 'ecommRefNo', 'mercId', 'mercCd', 'consUsernameMerchant', 'coCcyAmt', 'createdDt', 'issuerCode', 'mercRefNo', 'paySts', 'payBnkRefNo')
    if not bool(rows):
        return Response(json.dumps({'responseCode': 'MBDD01', 'responseMessage': 'INVALID_PARAMETER', 'responseDescription': 'query result is empty'}), mimetype='application/json')
    # for row in rows:
    # l = dir(rows)
    # pprint(l)
    # pprint(rows)
    # d = rows.__dict__
    # print ("====>>>>", l)
    # admin_merchant = cur.execute('SELECT merchant_code from mbdd_admin_merchant where id = ?', (id,))
    # db_version = cur.fetchone()
    cur.close()
    thislist = []
    # thislist.append({"name": "Bank Mandiry", "code": "BM", "icon": "/static/bankmandiri-icon.png", "token": ""})
    # thislist.append({"name": "Cimb Niaga", "code": "BM", "icon": "/static/bankmandiri-icon.png", "token": ""})
    # thislist.append({"name": "Bank Mandiry", "code": "BM", "icon": "/static/bankmandiri-icon.png", "token": ""})
    # y = json.dumps(thislist)
    #     >>> for row in cur.fetchall():
    # ...     results.append(dict(zip(columns, row)))
    # .
    # thislist.append(dict(zip(columns, rows)))
    # y = json.dumps(thislist, indent=2)
    data = dict(zip(columns, rows))
    r = {
        'responseCode': 'MBDD00',
        'responseMessage': 'SUCCESS',
        'responseDescription': 'SUCCESS',
        'responseValidation': {
            'mercCd': data['mercCd'],
            'consUsernameMerchant': data['consUsernameMerchant']
        },
        'data': data
    }
    y = json.dumps(r, indent=2, default=default)
    # print("environment==>", os.environ['FLASK_ENV'], "okeee")
    # logging.debug("env===> '%s' okeh.",os.environ['FLASK_ENV'])
    # logging.debug("env===>asdfdaf")
    return Response(y, mimetype='application/json')