#!/usr/bin/env python3

from bot.tweets import Tweet
from bot.constants import SEARCH_TERM, USERNAME, PASSWORD

__author__="Collins Kigen"
__copyright__="Copyright 2022"
__credits__=["Collins Kigen"]
__license__="GPL"
__version__="1.0.0"
__maintainer__="Collins Kigen"
__email__="ckigen.k@gmail.com"

inst = Tweet()
inst.land_first_page()
inst.login(USERNAME, PASSWORD)
inst.search(SEARCH_TERM)
inst.scroll_scrape_all_tweets()
inst.save_data()