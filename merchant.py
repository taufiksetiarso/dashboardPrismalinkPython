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

bp = Blueprint("merchant", __name__, url_prefix="/merchant")
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
@bp.route("/detail-limit")
def fetchOneLimit():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""SELECT
            a.limit_min_trx_daily,
            a.limit_trx_daily
            from mdo_merchant_limit a
            where a.merchant_id='%s'
            """ % (request.args.get('id')))
    except:
        logging.debug("I can't SELECT from mdo_merchant_limit")
    row = cur.fetchone()
    cur.close()
    if not bool(row):
        return Response(json.dumps({'responseCode': 'MBDD01', 'responseMessage': 'INVALID_PARAMETER', 'responseDescription': 'query result is empty'}), mimetype='application/json')
    columns = (
        'limitMinTrxDaily',
        'limitTrxDaily'
    )
    data = dict(zip(columns, row))
    r = {
        'responseCode': 'MBDD00',
        'responseMessage': 'SUCCESS',
        'responseDescription': 'SUCCESS',
        'responseValidation': {},
        'data': data
    }
    y = json.dumps(r, indent=2, default=default)
    return Response(y, mimetype='application/json')
    
@bp.route("/detail")
def fetchOne():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""SELECT
            a.id,
            a.merchant_id,
            a.inst_cd,
            a.merchant_mobile_no,
            a.merchant_email,
            a.created_dt
            from ecom_merc_ecomm a
            where a.id='%s'
            """ % (request.args.get('id')))
    except:
        logging.debug("I can't SELECT from ecom_merc_ecomm")
    rows = cur.fetchone()
    ecom_merc_ecomm_columns = (
        'id',
        'merchantId',
        'instCd',
        'merchantMobileNo',
        'merchantEmail',
        'createdDt'
    )
    if not bool(rows):
        return Response(json.dumps({'responseCode': 'MBDD01', 'responseMessage': 'INVALID_PARAMETER', 'responseDescription': 'query result is empty'}), mimetype='application/json')
    cur.close()
    ecom_merc_ecomm_data = dict(zip(ecom_merc_ecomm_columns, rows))

    # open cursoer
    cur = db.cursor()
    try:
        cur.execute("""SELECT
            a.cd,
            a.nm,
            a.addr,
            a.website
            from pay_inst a
            where a.cd='%s'
            """ % (ecom_merc_ecomm_data['instCd']))
    except:
        logging.debug("I can't SELECT from pay_inst")
    rows = cur.fetchone()
    # close cursoer
    cur.close()
    pay_inst_columns = (
        'cd',
        'nm',
        'addr',
        'website'
    )
    pay_inst_data = dict(zip(pay_inst_columns, rows))
    ecom_merc_ecomm_data.update(pay_inst_data)
    r = {
        'responseCode': 'MBDD00',
        'responseMessage': 'SUCCESS',
        'responseDescription': 'SUCCESS',
        'responseValidation': {},
        'data': ecom_merc_ecomm_data
    }
    y = json.dumps(ecom_merc_ecomm_data, indent=2, default=default)
    logging.debug(ecom_merc_ecomm_data)
    return Response(y, mimetype='application/json')
@bp.route("/cred")
def fetchOneCred():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""SELECT
            a.id,
            a.merc_ecomm_id,
            a.key_encrypt,
            a.valid_from,
            a.valid_to,
            a.status,
            a.created_dt,
            a.key_id
            from ecom_merc_ecomm_id a
            where a.merc_ecomm_id='%s'
            """ % (request.args.get('id')))
    except:
        logging.debug("I can't SELECT from ecom_merc_ecomm")
    rows = cur.fetchall()
    cur.close()
    columns = (
        'merchantId',
        'mercEcommId',
        'keyEncrypt',
        'validFrom',
        'validTo',
        'status',
        'createdDt',
        'keyId'
    )
    if not bool(rows):
        return Response(json.dumps({'responseCode': 'MBDD01', 'responseMessage': 'INVALID_PARAMETER', 'responseDescription': 'query result is empty'}), mimetype='application/json')
    vo = {}
    data = {}
    for r in rows:
        row = dict(zip(columns, r))
        if row['status'] == 'UPDATED':
            vo['merchantSecretKey'] = row['keyEncrypt']
            data = row
        elif row['status'] == 'NEW':
            vo['newMerchantSecretKey'] = row['keyEncrypt']
    
    data.update(vo)
    cur = db.cursor()
    try:
        cur.execute("""SELECT
            a.frontend_callback_url,
            a.backend_callback_url
            from ecom_merc_ecomm a
            where a.id='%s'
            """ % (data['mercEcommId']))
    except:
        logging.debug("I can't SELECT from ecom_merc_ecomm")
    row = cur.fetchone()
    columns = (
        'frontendCallbackUrl',
        'backendCallbackUrl'
    )

    dataMerchant = dict(zip(columns, row))
    cur = db.close()
    data.update(dataMerchant)

    # open cursoer
    # cur = db.cursor()
    # try:
    #     cur.execute("""SELECT
    #         a.cd,
    #         a.nm,
    #         a.addr,
    #         a.website
    #         from pay_inst a
    #         where a.cd='%s'
    #         """ % (ecom_merc_ecomm_data['instCd']))
    # except:
    #     logging.debug("I can't SELECT from pay_inst")
    # rows = cur.fetchone()
    # close cursoer
    # cur.close()
    # pay_inst_columns = (
    #     'cd',
    #     'nm',
    #     'addr',
    #     'website'
    # )
    # pay_inst_data = dict(zip(pay_inst_columns, rows))
    # ecom_merc_ecomm_data.update(pay_inst_data)
    r = {
        'responseCode': 'MBDD00',
        'responseMessage': 'SUCCESS',
        'responseDescription': 'SUCCESS',
        'responseValidation': {},
        'data': data
    }
    y = json.dumps(r, indent=2, default=default)
    return Response(y, mimetype='application/json')