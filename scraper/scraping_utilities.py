import requests
from bs4 import BeautifulSoup
import re


def get_year(aria_label: str):
    search = re.search(r"(\d{4})", aria_label)
    if search is None:
        return 2022
    else:
        return int(search.group(0))


def get_versions(url: str):
    query = requests.get(url)
    html = BeautifulSoup(query.text)
    versions = html.find("div", {"id": "versions"}).find_all('a')
    version_urls = [v["href"] for v in versions]
    labels = [v["aria-label"] for v in versions]
    version_words = [get_version_word(v_url) for v_url in version_urls]
    version_years = [get_year(label) for label in labels]
    next_url = get_next_url(html)
    return version_words, version_years, next_url


def get_next_url(html: BeautifulSoup):
    voisinages = html.find("div", {"id": "voisinage"})
    mot_actif = voisinages.find('li', attrs={'class': 'motActif'}).text.split(',')[0].lstrip()
    voisinages = voisinages.find_all("a")
    words = [v.text.split(',')[0] for v in voisinages]
    i = words.index(mot_actif)
    if i == len(voisinages) - 1:
        return "END"
    else:
        next_article_id = voisinages[i + 1]["href"].split('/')[-1]
        return f"https://www.dictionnaire-academie.fr/{next_article_id}"


def get_version_word(v_url: str):
    a = requests.get(f"https://www.dictionnaire-academie.fr{v_url}")
    soup = BeautifulSoup(a.text)
    mot_nouveau = soup.find("title").text.split("|")[0][:-1]
    return mot_nouveau


def get_article_id(url: str):
    return url.split('/')[-1]
