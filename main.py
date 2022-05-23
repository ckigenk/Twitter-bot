from bot.tweets import Tweet
from bot.constants import SEARCH_TERM, USERNAME, PASSWORD

inst = Tweet()
inst.land_first_page()
inst.login(USERNAME, PASSWORD)
inst.search(SEARCH_TERM)
inst.scroll_scrape_all_tweets()
inst.save_data()