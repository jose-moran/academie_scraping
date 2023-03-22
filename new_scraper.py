import json
from string import ascii_uppercase as asu

import numpy as np

from scraper.scraping_utilities import get_versions

scrape_dict = json.load(open("./scraped_dict.json", "r"))

keys = list(scrape_dict.keys())


def get_letter_list(letter, version, key_list):
    id_list = np.array([f"A{version}{letter}{str(r).zfill(4)}" for r in range(1, 10000)])
    id_list = id_list[~np.isin(id_list, key_list)]
    return id_list


for version in [9, 8]:
    for letter in asu:
        id_list = get_letter_list(letter, version, keys)
        for article_id in id_list:
            url = f"https://www.dictionnaire-academie.fr/article/{article_id}"
            res_dict = get_versions(article_id)
            if len(res_dict["words"]) == 0:
                break
            print(article_id)
            scrape_dict[article_id] = res_dict

json.dump(scrape_dict, open("./scraped_dict.json", "w"))
