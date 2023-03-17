import pytest

from scraper.scraping_utilities import get_year, get_version_word, get_versions


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
    version_words, version_years = get_versions(roi_url)
    assert set(version_words) == {"roi", "roy"}
    assert set(version_years) == {1694, 1718, 1740, 1762, 1798, 1835, 1878, 1935, 2022}
