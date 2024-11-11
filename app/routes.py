# app/routes.py

from flask import Blueprint, request, jsonify, current_app
from app.search_crawler import SearchAPICrawler
from app.content_extractor import ContentExtractor
from app.webhook_handler import send_webhook_to_botpress
from app.summarizer import summarize_content
import json
import asyncio

bp = Blueprint('main', __name__)

@bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    query = data.get('query')
    pages = data.get('pages', 1)

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    if not 1 <= pages <= 10:
        return jsonify({"error": "pages must be between 1 and 10"}), 400
    
    # Run the search operation and extraction asynchronously
    asyncio.run(process_search(query, pages))

    return jsonify({"status": "Processing Started"}), 202

async def process_search(query, pages):
    crawler = SearchAPICrawler()
    search_results = crawler.crawl(query, pages=pages)

    extractor = ContentExtractor(search_results)
    extractor.extract_content()
    content = extractor.get_extracted_content()

    # GPT summarizer
    json_content = json.dumps(content, indent=2)
    summary = summarize_content(query, json_content)

    final_result = {
        "WebSearch": summary
    }

    #send results back to botpress
    await send_webhook_to_botpress(final_result)

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200