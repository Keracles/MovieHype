import json
from bs4 import BeautifulSoup
import requests
import pandas as pd

url_test1 = "https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars"
url_test = "https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-specific-technical-role/director"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get(url):
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.OK :
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    return None

def parse_number(str):
    str = str.replace("$", "")
    str = str.replace(",", "")
    str = str.strip()
    floate = int(str)


    return floate

def parse_page(url):
    soup = get(url)
    dict = {}
    if soup is not None :
        soup = soup.find("tbody")
        soup = soup.find_all("tr")
        for section in soup :
            name_director = section.find("a").contents[0].replace('"','')
            section = section.find_all(attrs={"align": "right"})
            worldwide_box_office = parse_number(section[0].contents[0])
            dict[name_director] = worldwide_box_office
    return dict 


def get_all():
    final_dict = {}
    dicts = []
    for i in range(1,17000,100):
        dicts.append(parse_page(url_test + f"/{i}"))
    for dict in dicts :
        final_dict.update(dict)


    df = pd.DataFrame(list(final_dict.items()),
                   columns=['Director_Name', 'Worldwide_box_office'])
    df.to_csv("director_scrap.csv")



get_all()