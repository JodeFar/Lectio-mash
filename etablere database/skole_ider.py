import requests
from bs4 import BeautifulSoup
import re


def orden_skole_navn(skole_navn):
    try:
        lms = skole_navn.split(" ")
        return " ".join([x[0].upper() + x[1:] for x in lms])
    except:
        return skole_navn
def find_skole_id(min_skoles_navn, skoler):
    pattern_skole = re.compile(min_skoles_navn)
    pattern_skole_nummer = re.compile(r"\d\d")
    for x in skoler:
        match = pattern_skole.finditer(str(x))
        for y in match:
            skole_nummer_match = pattern_skole_nummer.finditer(str(x))
            for t in skole_nummer_match:
                print("registeret skole id er", t.group())
                return t.group()

def fo_skole_id(skole_navn):
    min_skoles_navn = orden_skole_navn(skole_navn)
    url = f'https://www.lectio.dk/lectio/login_list.aspx'
        # Get the initial login page to obtain the ViewState and EventValidation values and ASP.net session value
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    skoler = soup.findAll("div",{"class":"buttonHeader"})
    return find_skole_id(min_skoles_navn, skoler)


