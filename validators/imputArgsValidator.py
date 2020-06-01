from dateutil.parser import parse

from exceptions.exceptions import CurrencyError


def validate_convert_fields(from_currency: str, to: str, amount: str, time: str):
    msg = ''
    if from_currency is None or len(from_currency.strip()) == 0:
        msg += 'From Currency param is mandatory! '
    if to is None or len(to.strip()) == 0:
        msg += 'To Currency param is mandatory! '
    if amount is None or len(amount.strip()) == 0:
        msg += 'Amount param is mandatory! '

    if len(msg.strip()) > 0:
        raise CurrencyError(msg)

    try:
        a = float(amount)
        if a < 0:
            msg += 'Amount must be positive number! '
    except ValueError:
        msg += 'Amount must be a number! '

    try:
        if len(time.strip()) > 0:
            parse(time)
    except ValueError:
        msg += 'Invalid Date Format! Valid form - YYYY-mm-dd! '

    if len(msg.strip()) > 0:
        raise CurrencyError(msg)


def validate_rates_fields(base: str, to: str, time: str):
    msg = ''
    if base is None or len(base.strip()) == 0:
        msg += 'Base is mandatory! '

    if len(msg.strip()) > 0:
        raise CurrencyError(msg)

    try:
        if len(time.strip()) > 0:
            parse(time)
    except ValueError:
        msg += 'Invalid Date Format! Valid form - YYYY-mm-dd! '

    if len(msg.strip()) > 0:
        raise CurrencyError(msg)