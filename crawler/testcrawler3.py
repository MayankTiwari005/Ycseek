import requests
from bs4 import BeautifulSoup
import json
import pymongo
from urllib.parse import urljoin
import os
from dotenv import load_dotenv

load_dotenv()
class Crawler():
    def __init__(self):
        connect_uri = os.environ.get('MONGODB_URI')
        
        self.client = pymongo.MongoClient(connect_uri)
        self.db = self.client.Crawlex
        self.search_results = []
        self.visited = set()

    def crawl(self, url, depth):
        # skip if already visited
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            print(f"Crawling URL: {url} at depth {depth}")
            response = requests.get(url, headers={'user-agent': 'comb-search'}, timeout=10)
        except:
            print(f'failed to process\n {url}')
            return

        content = BeautifulSoup(response.text, 'lxml')

        try:
            title = content.find('title').text
            description = ''
            for tag in content.findAll():
                if tag.name == 'p':
                    description += tag.text.strip().replace('\n', '')
        except:
            return

        # only save if there's actual content worth saving
        if title and description:
            result = {
                'url': url,
                'title': title,
                'description': description
            }
            self.search_results.append(result)
            print(f'Saved: {title[:50]}')

        if depth == 0:
            return

        links = content.findAll('a')
        for link in links:
            try:
                href = link['href']
                full_url = urljoin(url, href)

                # only follow ycombinator links, skip anchors and mailto i.e, means follow ups of ycombinator, differ for each website
                if 'ycombinator.com' in full_url and 'http' in full_url:
                    self.crawl(full_url, depth - 1)
            except KeyError:
                pass

    def insert_results(self):
        if not self.search_results:
            print('No results to insert!')
            return

        search_results = self.db.search_results

        # no duplicates if you run it twice
        for result in self.search_results:
            search_results.update_one(
                {'url': result['url']},
                {'$setOnInsert': result},
                upsert=True
            )

        # only create index if it doesn't exist
        existing_indexes = search_results.index_information()
        if 'search_results' not in existing_indexes:
            search_results.create_index([
                ('url', pymongo.TEXT),
                ('title', pymongo.TEXT),
                ('description', pymongo.TEXT)
            ], name='search_results', default_language='english')
            print('Index created.')

        self.client.close()
        print(f'Inserted {len(self.search_results)} results into MongoDB.')

    def print_data(self):
        for entry in self.search_results:
            print(json.dumps(entry))
        print(f'\nEntries Scrapped: {len(self.search_results)}')


crawler = Crawler()
crawler.crawl('https://news.ycombinator.com', depth=1)
crawler.insert_results()
crawler.print_data()
