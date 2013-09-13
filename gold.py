import requests
from lxml.html.soupparser import fromstring


purities = ["TT", 24, 22, 18]


def fetch_gold_prices():
    tree = fromstring(
        requests.get(
            "http://www.khaleejtimes.com/forex.asp"
        ).text
    )
    
    futurebox = tree.xpath("//div[@id='futurbox']")[0]
    date = futurebox.xpath(
        "table//tr[2]"
    )[0].text_content().strip()
    all_prices = {}
    for purity in purities:
        prices = {}
        quality_prices = futurebox.xpath(
            "table//tr/td/span[text()='%s']/../../td/text()" % purity
        )[1:4]

        prices["morning"], prices["evening"], prices["yesterday"] = map(float, quality_prices)

        all_prices[purity] = prices

    return {
        "date": date,
        "prices": all_prices
    }


if __name__ == "__main__":
    
    price_details = fetch_gold_prices()
    
    print "Gold Prices for %s" % price_details["date"]
    
    all_prices = price_details["prices"]    
    for purity in purities:
        prices = all_prices[purity]
        print "%s:" % purity
        for time, price in prices.items():
            print "  %s - %.2f" % (('{:>%d}' % len("yesterday")).format(time), price)
