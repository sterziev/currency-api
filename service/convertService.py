from exceptions.exceptions import CurrencyError
from models.currency import Currency
from dateutil.parser import parse


def convert(from_currency: str, to: str, amount: str, date: str):
    try:
        from_currency = from_currency.upper()
        to = to.upper()
        currencies = [from_currency, to]
        rates = Currency.query.filter(Currency.name.in_(currencies),
                                      Currency.date == parse(date)).all()
        fromRate = None
        toRate = None
        for rate in rates:
            if rate.name == from_currency:
                fromRate = rate
            if rate.name == to:
                toRate = rate

        print(fromRate)
        if fromRate is None:
            raise CurrencyError('Currency {} not found'.format(from_currency))
        if toRate is None:
            raise CurrencyError('Currency {} not found'.format(to))

        amountInEuro = float(amount) / fromRate.rate
        amountInTo = amountInEuro * toRate.rate
        return {"from": from_currency,
                "to": to,
                "from amount": amount,
                "to amount": amountInTo}

    except Exception as e:
        print(str(e))
        raise CurrencyError(str(e))
