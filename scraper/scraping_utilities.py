import requests
from bs4 import BeautifulSoup
import re


def get_year(aria_label: str):
    search = re.search(r"(\d{4})", aria_label)
    if search is None:
        return 2022
    else:
        return int(search.group(0))


def get_versions(article_id: str):
    url = f"https://www.dictionnaire-academie.fr/article/{article_id}"
    query = requests.get(url)
    html = BeautifulSoup(query.text)
    versions = html.find("div", {"id": "versions"}).find_all('a')
    version_urls = [v["href"] for v in versions]
    labels = [v["aria-label"] for v in versions]
    version_words = [get_version_word(v_url) for v_url in version_urls]
    version_years = [get_year(label) for label in labels]
    return {"words": version_words, "years": version_years}


def get_voisinages(article_id: str):
    url = f"https://www.dictionnaire-academie.fr/article/{article_id}"
    query = requests.get(url)
    html = BeautifulSoup(query.text)
    voisinages = html.find("div", {"id": "voisinage"})
    return [v["href"].split('/')[-1] for v in voisinages.find_all("a")]



def get_version_word(v_url: str):
    a = requests.get(f"https://www.dictionnaire-academie.fr{v_url}")
    soup = BeautifulSoup(a.text)
    mot_nouveau = soup.find("title").text.split("|")[0][:-1]
    return mot_nouveau


def get_article_id(url: str):
    return url.split('/')[-1]
