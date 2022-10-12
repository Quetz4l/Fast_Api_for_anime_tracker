import requests
from bs4 import BeautifulSoup as bs
import lxml
import json

def get_soup(url):
    html = requests.get(url)
    soup = bs(html.text, 'lxml')
    return soup


def get_anime_from_jikan(jikan_anime_id):
    response = requests.get(f"https://api.jikan.moe/v4/anime/{jikan_anime_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return False