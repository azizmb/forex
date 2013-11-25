import argparse

import requests
from lxml.html.soupparser import fromstring


def preev(amount, base, to):
    if base.lower() == "btc":
        currency = to
    else:
        currency = base

    scrape_link = "http://preev.com/rate/units:btc,%(currency)s/source:bitstamp"

    response = requests.get(
        scrape_link % {"currency": currency.lower()}
    )

    rate = float(response.json()["rate"])

    if base.lower() == "btc":
        currency_rate = rate
    else:
        currency_rate = 1.0 / rate

    return amount * currency_rate


def google_finance(amount, base, to):
    google_finance_link = "https://www.google.com/finance/converter?a=%(amount)f&from=%(base)s&to=%(to)s"

    response = requests.get(
        google_finance_link % {"amount": amount, "base": base.upper(), "to": to.upper()}
    )
    tree = fromstring(response.text)

    value_text = tree.xpath(
        "//div[@id='currency_converter_result']/span/text()"
    )[0]

    return float(value_text.split(" ", 2)[0])


def get_scraper(*currencies):
    scrapers = {
        "btc": preev
    }

    for currency in currencies:
        try:
            return scrapers[currency]
        except KeyError:
            pass
    else:
        return google_finance


def convert_amount(amount, base, to):

    scraper = get_scraper(base, to)

    return scraper(amount, base, to)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("amount", help="the amount you want to convert", type=float)
    parser.add_argument("base", help="the base currency")
    parser.add_argument("to", help="the currency to convert to")
    args = parser.parse_args()

    print convert_amount(args.amount, args.base, args.to)
