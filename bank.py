import logging
import os
from flaskr.db_postgresql import get_db
from flask import (
    Blueprint,
    Response
)
import json

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


bp = Blueprint("bank", __name__, url_prefix="/bank")

@bp.route("/fetch-all")
def fetch_all():
    db = get_db()
    cur = db.cursor()
    id = '4028811b6d3cabd5016d3cad47e'
    user_id = '4028d86c6d386583016d3865bc'
    try:
        cur.execute("SELECT merchant_code from mbdd_admin_merchant where id='%s' and user_id='%s' " % (id,user_id))
    except:
        print("I can't SELECT from bar")
    rows = cur.fetchone()
    # for row in rows:
    print ("   ", rows[0])
    # admin_merchant = cur.execute('SELECT merchant_code from mbdd_admin_merchant where id = ?', (id,))
    # db_version = cur.fetchone()
    cur.close()
    thislist = []
    thislist.append({"name": "Bank Mandiry", "code": "BM", "icon": "/static/bankmandiri-icon.png", "token": ""})
    thislist.append({"name": "Cimb Niaga", "code": "BM", "icon": "/static/bankmandiri-icon.png", "token": ""})
    thislist.append({"name": "Bank Mandiry", "code": "BM", "icon": "/static/bankmandiri-icon.png", "token": ""})
    y = json.dumps(thislist)
    print("environment==>", os.environ['FLASK_ENV'], "okeee")
    logging.debug("env===> '%s' okeh.",os.environ['FLASK_ENV'])
    logging.debug("env===>asdfdaf")
    return Response(y, mimetype='application/json')