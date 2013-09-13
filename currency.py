import argparse

import requests
from lxml.html.soupparser import fromstring


def convert_amount(amount, base, to):
    google_finance_link = "https://www.google.com/finance/converter?a=%(amount)f&from=%(base)s&to=%(to)s"
    
    response = requests.get(
        google_finance_link % {"amount": amount, "base": base.upper(), "to": to.upper()}
    )
    tree = fromstring(response.text)
    
    value_text = tree.xpath(
        "//div[@id='currency_converter_result']/span/text()"
    )[0]

    return float(value_text.split(" ", 2)[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("amount", help="the amount you want to convert", type=float)
    parser.add_argument("base", help="the base currency")
    parser.add_argument("to", help="the currency to convert to")
    args = parser.parse_args()
    
    print convert_amount(args.amount, args.base, args.to)
