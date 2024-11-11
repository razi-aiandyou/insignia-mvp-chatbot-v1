# app/content_extractor.py

import requests
from bs4 import BeautifulSoup
from flask import current_app
import json

class ContentExtractor:
    def __init__(self, results):
        self.results = results
        self.extracted_content = []

    def extract_content(self):
        for result in self.results:
            try:
                response = requests.get(result['url'], timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract content
                content = soup.get_text(separator='\n', strip=True)
                
                self.extracted_content.append({
                    'url': result['url'],
                    'title': result['title'],
                    'description': result['description'],
                    'content': content
                })
                current_app.logger.info(f"Extracted content from: {result['url']}")
            except Exception as e:
                current_app.logger.error(f"Failed to extract content from {result['url']}: {e}")

    def save_to_json(self, filename='extracted_content.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_content, f, ensure_ascii=False, indent=4)
        current_app.logger.info(f"Saved extracted content to {filename}")

    def get_extracted_content(self):
        return self.extracted_content