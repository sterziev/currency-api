from flask import Blueprint, jsonify
from exceptions.exceptions import CurrencyError
from datetime import date

error = Blueprint('errors', __name__)


@error.app_errorhandler(CurrencyError)
def handle_exception(e):
    print('in error handler')
    if hasattr(e, 'message'):
        msg = e.message
    else:
        msg = str(e)

    if len(msg) == 0:
        msg = 'Something goes wrong!'

    response = jsonify({
        "code": 400,
        "message": msg,
        "timestamp": date.today()
    })
    return response, 400
