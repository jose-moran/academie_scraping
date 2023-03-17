import json

from scraper.scraping_utilities import get_versions, get_article_id

scrape_dict = {}
current_url = "https://www.dictionnaire-academie.fr/article/A9A0001"

next_url = ""


while next_url != "END":
    version_words, version_years, next_url = get_versions(current_url)
    print(version_words[-1], end=", ")
    art_id = get_article_id(current_url)
    scrape_dict[art_id] = {"words": version_words, "years": version_years}
    current_url = next_url

json.dump(scrape_dict, open("./scraped_dict.json", "w"))