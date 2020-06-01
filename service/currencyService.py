import requests
from datetime import date
from app import db
from exceptions.exceptions import CurrencyError
from models.currencySync import CurrencySync
from models.currency import Currency
from dateutil.parser import parse

baseUrl = 'http://data.fixer.io/api/{}?access_key={}'
accessKey = ''
time = 'latest'


def getCurrencyRates():
    if getInfoForToday().isSynced is True:
        print("Get Rates from DB")
        rates = getRatesFromDb()
    else:
        print("Get Rates from Api")
        rates = getFromApiAndCommit()
        syncToday()
    return rates


def getRatesFromDb():
    try:
        rates = Currency.query.filter_by(date=date.today()).all()
        return rates
    except Exception as e:
        print(str(e))
        raise CurrencyError(str(e))


def getInfoForToday():
    try:
        synced: CurrencySync = CurrencySync.query.filter_by(date=date.today()).first()
        if synced is None:
            raise CurrencyError('Missing Status in DB!')
        return synced
    except Exception as e:
        print(str(e))
        raise CurrencyError(str(e))


def syncToday():
    try:
        print("Mark today as Synced")
        synced: CurrencySync = CurrencySync.query.filter_by(date=date.today()).first()
        synced.isSynced = True
        db.session.add(synced)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(str(e))
        raise CurrencyError(str(e))


def getFromApiAndCommit():
    rates = []
    url = baseUrl.format(time, accessKey)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json = response.json()
            ratesKvp = json["rates"]
            date = json["date"]
            for rate in ratesKvp:
                r = Currency(name=rate, rate=ratesKvp[rate], date=date)
                rates.append(r)
                db.session.add(r)
            db.session.commit()
        else:
            print("Failed to get rates, {}".format(response.status_code))
            raise CurrencyError("Failed to get rates from API, {}".format(response.status_code))
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(str(e))
        raise CurrencyError(str(e))

    return rates


def get_rates(base: str, to: str, time: str):
    to_array = []
    base = base.upper()

    if to is not None and len(to.strip()) > 0:
        to_array = to.split(',')
        to_array = [currency.upper() for currency in to_array]
    to_array.insert(0, base)

    if len(to_array) > 1:
        rates = Currency.query.filter(Currency.name.in_(to_array),
                          Currency.date == parse(time)).all()
    else:
        rates = Currency.query.filter(Currency.date == parse(time)).all()

    fromRate = None
    for rate in rates:
        if rate.name == base:
            fromRate = rate
            break

    if fromRate is None:
        raise CurrencyError('Base Currency {} not found'.format(base))

    rates_dict = { rate.name: rate.rate / fromRate.rate for rate in rates if rate.name != fromRate.name}
    response = {
        'base': base,
        'date': time,
        'rates': rates_dict
    }

    return response
