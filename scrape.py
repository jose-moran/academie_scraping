import json
import requests
import re

from scraper.scraping_utilities import get_versions,  get_voisinages

scrape_dict = json.load(open("./scraped_dict.json", "r"))

current_id = list(scrape_dict.keys())[-1]

keep_going = True
while keep_going:
    try:
        print(current_id)
        scrape_dict[current_id] = get_versions(current_id)
        new_ids = get_voisinages(current_id)
        not_scraped = list(filter(lambda x: x not in scrape_dict.keys(), new_ids))
        if len(not_scraped) == 0:
            last_current_edition = list(filter(lambda x: x.startswith('A9'), scrape_dict.keys()))[-1]
            new_tag = int(re.match(r"A9[A-Z]([0-9]*)", last_current_edition).groups(0)[0])+1
            new_tag = str(new_tag).zfill(4)
            last_prev_edition = list(filter(lambda x: x.startswith('A8'), scrape_dict.keys()))[-1]
            new_prev_tag = int(re.match(r"A8[A-Z]([0-9]*)", last_prev_edition).groups(0)[0])+1
            new_prev_tag = str(new_prev_tag).zfill(4)
            new_id = f"{last_current_edition[:3]}{new_tag}"
            new_prev_id = f"{last_prev_edition[:3]}{new_prev_tag}"
            url1 = f"https://www.dictionnaire-academie.fr/article/{new_id}"
            query1 = requests.get(url1)
            url2 = f"https://www.dictionnaire-academie.fr/article/{new_prev_id}"
            query2 = requests.get(url2)
            if query1.status_code != 404:
                current_id = new_id
            elif query2.status_code != 404:
                current_id = new_prev_id
            else:
                print(f"STOPPED AT {current_id}")
                keep_going = False
        else:
            current_id = not_scraped[0]
    except:
        keep_going = False

json.dump(scrape_dict, open("./scraped_dict.json", "w"))