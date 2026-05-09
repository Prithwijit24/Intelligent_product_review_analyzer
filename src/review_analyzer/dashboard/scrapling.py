from scrapling.fetchers import Fetcher, AsyncFetcher, StealthyFetcher, DynamicFetcher
StealthyFetcher.adaptive = True
p = StealthyFetcher.fetch('https://example.com', headless=True, network_idle=True)  # Fetch website under the radar!
products = p.css('.product', auto_save=True)                                        # Scrape data that survives website design changes!
products = p.css('.product', adaptive=True)                                         # Later, if the website structure changes, pass `adaptive=True` to find them!