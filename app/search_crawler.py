import requests
from bs4 import BeautifulSoup
import time
from flask import current_app

class SearchAPICrawler:
    def __init__(self):
        self.api_key = current_app.config['GOOGLE_API_KEY']
        self.search_engine_id = current_app.config['GOOGLE_SEARCH_ENGINE_ID']
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.visited_urls = set()
        self.results = []

    def search(self, query, num=10, start=1):
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num,
            'start': start
        }
        response = requests.get(self.base_url, params=params)
        json_response = response.json()
        
        # Print out the full response for debugging
        current_app.logger.info(f"API Response: {json_response}")
        
        return json_response

    def crawl_page(self, url):
        if url in self.visited_urls:
            return

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract information from the page
            title = soup.title.string if soup.title else "No title"
            description = soup.find('meta', attrs={'name': 'description'})
            description = description['content'] if description else "No description"
            
            self.results.append({
                'url': url,
                'title': title,
                'description': description
            })
            
            self.visited_urls.add(url)
            current_app.logger.info(f"Crawled: {url}")
        except Exception as e:
            current_app.logger.error(f"Error crawling {url}: {e}")

    def crawl(self, query, pages=1):
        for i in range(pages):
            start = i * 10 + 1
            search_results = self.search(query, num=10, start=start)
            
            if 'items' not in search_results:
                current_app.logger.warning("No more results or error in API response")
                break
            
            for item in search_results['items']:
                self.crawl_page(item['link'])
            
            time.sleep(1)  # Respect rate limits

        return self.results