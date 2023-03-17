import json

from scraper.scraping_utilities import get_versions, get_article_id

scrape_dict = json.load(open("./scraped_dict.json", "r"))
current_url = "https://www.dictionnaire-academie.fr/article/A9A0713"

next_url = ""

i = 1
while next_url != "END":
    try:
        version_words, version_years, next_url = get_versions(current_url)
        print(version_words[-1], end=", ")
        art_id = get_article_id(current_url)
        if art_id in scrape_dict.keys():
            break
        scrape_dict[art_id] = {"words": version_words, "years": version_years}
        current_url = next_url
        if i % 5 == 0:
            print("\n")
        i += 1
    except:
        break


art_id = get_article_id(current_url)
print(f"Finished at {art_id}")
json.dump(scrape_dict, open("./scraped_dict.json", "w"))