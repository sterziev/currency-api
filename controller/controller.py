from datetime import date
from flask import Blueprint, request, jsonify
import service.currencyService as currencyService
import service.convertService as convertService
from exceptions.exceptions import CurrencyError
from validators.imputArgsValidator import validate_convert_fields, validate_rates_fields

controller = Blueprint('controller', __name__)


@controller.route("/")
def seed_currencies():
    result = currencyService.getCurrencyRates()
    response = [currency.serialize() for currency in result]
    return jsonify(response)


@controller.route("/rates")
def get_rates():
    base = request.args.get('base')
    to = request.args.get('to')
    time = request.args.get('date', str(date.today()))
    validate_rates_fields(base, to, time)
    print("convert with params:", base, to, time)
    return jsonify(currencyService.get_rates(base, to, time))

@controller.route('/convert')
def convert():
    from_currency = request.args.get('from')
    to = request.args.get('to')
    amount = request.args.get('amount')
    time = request.args.get('date', str(date.today()))
    validate_convert_fields(from_currency, to, amount, time)
    print("convert with params:", from_currency, to, amount, time)
    return jsonify(convertService.convert(from_currency, to, amount, time))


@controller.route('/error')
def raise_error():
    raise CurrencyError("error")
