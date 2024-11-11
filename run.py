# run.py

import argparse
from app import create_app
import requests

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the search and content extraction application.")
    parser.add_argument("query", help="The search query to use")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to crawl (default: 1)")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    app = create_app()
    
    # Store the arguments in the app config
    app.config['SEARCH_QUERY'] = args.query
    app.config['NUM_PAGES'] = args.pages
    
    # Start the Flask app in a separate thread
    from threading import Thread
    thread = Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False})
    thread.start()

    # Execute the search request
    response = requests.get('http://127.0.0.1:5000/search')
    print(response.json())