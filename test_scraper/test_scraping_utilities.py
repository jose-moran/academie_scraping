import pytest
import requests
from bs4 import BeautifulSoup

from scraper.scraping_utilities import get_year, get_version_word, get_versions, get_next_url, get_article_id


@pytest.fixture(name="roi_url")
def roi_url():
    return "https://www.dictionnaire-academie.fr/article/A9R2839"


def test_get_year():
    assert get_year("première édition 1694") == 1694
    assert get_year("édition actuelle") == 2022


def test_get_word():
    v_url = "/article/A1R0098-37"
    assert get_version_word(v_url) == "roy"


def test_get_versions(roi_url):
    version_words, version_years, url = get_versions(roi_url)
    assert set(version_words) == {"roi", "roy"}
    assert set(version_years) == {1694, 1718, 1740, 1762, 1798, 1835, 1878, 1935, 2022}


def test_next_url(roi_url):
    query = requests.get(roi_url)
    html = BeautifulSoup(query.text)
    assert get_next_url(html) == "https://www.dictionnaire-academie.fr/article/A9R2840"

    query2 = requests.get("https://www.dictionnaire-academie.fr/article/A6Z0043*")
    html = BeautifulSoup(query2.text)
    assert get_next_url(html) == "END"

    query3 = requests.get("https://www.dictionnaire-academie.fr/article/A8A0002")
    html = BeautifulSoup(query3.text)
    assert get_next_url(html) == "https://www.dictionnaire-academie.fr/article/A9A0002"

    query4 = requests.get("https://www.dictionnaire-academie.fr/article/A9A0144")
    html = BeautifulSoup(query4.text)
    assert get_next_url(html) == "https://www.dictionnaire-academie.fr/article/A9A0145*"

def test_article_id(roi_url):
    assert get_article_id(roi_url) == "A9R2839"
