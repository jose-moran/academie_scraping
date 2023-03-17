from tqdm import tqdm
import json

from scraper.scraping_utilities import get_versions, get_article_id

scrape_dict = {}
current_url = "https://www.dictionnaire-academie.fr/article/A9A0001"

next_url = ""


def generator(condition):
    while condition:
        yield


for _ in tqdm(generator(next_url != "END")):
    version_words, version_years, next_url = get_versions(current_url)
    id = get_article_id(current_url)
    scrape_dict[id] = {"words": version_words, "years": version_years}
    current_url = next_url

json.dump(scrape_dict, open("./scrape_results.json", "w"))
