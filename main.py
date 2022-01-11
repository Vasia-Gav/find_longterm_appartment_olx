import datetime
import aiohttp
import asyncio
from bs4 import BeautifulSoup, NavigableString
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('price_from', help='Нижняя граница цены в UAH, чтоб отсечь то, что уже смотрел например', nargs='?', default="5000")
parser.add_argument('price_to', help='Верхняя граница цены в UAH', nargs='?', default="9000")
parser.add_argument('min_size', help='Минимальная площадь хаты', nargs='?', default="30")
args = parser.parse_args()
price_from = args.price_from
price_to = args.price_to
sq_m = args.min_size


def parse_resp(r, f):
    links = []
    soup = BeautifulSoup(r)
    body_con = soup.find("section", {"id": "body-container"})

    if body_con.find("div", {"class": "emptynew"}):
        return []

    for el in body_con.find("div", {"class": "listHandler"}).children:
        if isinstance(el, NavigableString):
            continue
        a_tags = el.find_all("a", {"class", "vtop"})
        if not a_tags:
            continue
        links_ = [l.attrs["href"] for l in a_tags]
        links.extend(links_)
        f.writelines("\n".join(links_) + "\n")

    return links


async def main():
    results = []
    search_requests = [
        "центр",
        "пушкинская",
        "сумская",
        "гиршмана",
        "мироносицкая",
        "чернышевская",
        "конституции",
        "научная",
        "бекетова",
        "университет",
        "горького"  # Просто добавь воды
    ]
    with open("var/re_%s.txt" % datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"), "a+") as f:
        async with aiohttp.ClientSession() as session:
            for loc in search_requests:
                url = "https://www.olx.ua/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kharkov/" \
                      "q-" + loc + "/?search%5Bfilter_float_price%3Afrom%5D=" + price_from + "&search%5Bfilter_float_price%3Ato%5D=" + price_to + \
                      "&search%5Bfilter_float_total_area%3Afrom%5D=" + sq_m

                async with session.get(url) as resp:
                    r = await resp.text()
                    try:
                        results.extend(parse_resp(r, f))
                    except Exception as e:
                        print(e.args)


if __name__ == "__main__":
    asyncio.run(main())
