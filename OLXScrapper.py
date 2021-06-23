import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse_price(olx_price: str) -> float:
    """ Change price from (str)'xx.xx zl' to (float) xx.xx

    Args:
        olx_price (str): price in string (possible with currency)

    Returns:
        float: pure price
    """
    if olx_price.strip() == "Za darmo":
        return .0
    if olx_price.strip() == "Zamienię":
        return -1
    return float(olx_price.strip().replace(',', '.').
                 replace('zł', '').replace(' ', ''))


def olx_scrapper(url: str, nr_of_page: int = 5, url_to_hyperlink=False) -> pd.DataFrame:
    olx_request = requests.get(url)
    title, price, city, date, link = [], [], [], [], []
    if '?' in url:
        urlMultiWebSide = url+"&page="
    else:
        urlMultiWebSide = url+"?page="
    bs = BeautifulSoup(olx_request.content, 'html.parser')
    flefts = bs.find('div', class_='pager')
    try:
        numOfPage = int(flefts.find_all('span')[-3].get_text().strip())
    except Exception:
        numOfPage = 1
    if numOfPage > nr_of_page:
        numOfPage = nr_of_page
    pgNum = 1
    for page in [requests.get(urlMultiWebSide+str(num+1))
                 for num in range(numOfPage)]:
        print(f"scrappowanie strony {pgNum} z {numOfPage}")
        pgNum += 1
        bs = BeautifulSoup(page.content, 'html.parser')
        for offer in bs.find_all("div", class_="offer-wrapper"):
            title.append(offer.find(
                'td', class_="title-cell").find('h3').get_text().strip())
            link.append(offer.find(
                'td', class_="title-cell").find('a')['href'].split(';')[0])
            price.append(parse_price(offer.find(
                'p', class_="price").get_text()))
            footer = offer.find('td', class_="bottom-cell")
            city.append(footer.find_all('small')[0].get_text().strip())
            date.append(footer.find_all('small')[1].get_text().strip())
    bionicleData = pd.DataFrame({"title": title, "price": price,
                                 "city": city, "date": date, "link": link})
    if len(bionicleData.index) == 0:
        return r'''< div class="w3-panel w3-red" >
                               <h3>Uwaga< /h3 >
                               <p> Podany link jest nieprawidłowy lub nie da się go zescrapować (np zła kategoria: np. praca). < /p >
                               </div>'''
    if url_to_hyperlink:
        bionicleData.link = pd.Series(
            [f"<a href='{x}'>{x}</a>"
             for x in bionicleData.link])
    return bionicleData


if __name__ == '__main__':
    pass
