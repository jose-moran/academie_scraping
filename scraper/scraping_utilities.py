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
    next_url = get_next_url(html, current_word = version_words[-1])
    return version_words, version_years, next_url




def get_next_url(html: BeautifulSoup, current_word):
    voisinages = html.find("div", {"id": "voisinage"}).find_all("a")
    words =  [v.text.split(',')[0].split(' ')[0] for v in voisinages]
    i = words.index(current_word)
    if i == len(voisinages) - 1:
        return "END"
    else:
        next_article = re.search("/article/(\w*)", voisinages[i+1]["href"]).group(0)
        return f"https://www.dictionnaire-academie.fr{next_article}"

def get_version_word(v_url: str):
    a = requests.get(f"https://www.dictionnaire-academie.fr{v_url}")
    soup = BeautifulSoup(a.text)
    mot_nouveau = soup.find("title").text.split("|")[0][:-1]
    return mot_nouveau
