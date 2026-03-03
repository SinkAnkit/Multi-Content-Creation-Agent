import os
from pydantic import BaseModel, HttpUrl
from firecrawl import FirecrawlApp
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')

class ScrapeInput(BaseModel):
    requestId: str
    url: HttpUrl
    timestamp: int

config = {
    'type': 'event',
    'name': 'ScrapeArticle',
    'description': 'Scrapes article content using Firecrawl',
    'subscribes': ['scrape-article'],
    'emits': ['generate-content'],
    'input': ScrapeInput.model_json_schema(),
    'flows': ['content-generation']
}

async def handler(input, context):
    context.logger.info(f"🕷️ Scraping article: {input['url']}")

    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    # Firecrawl v4 uses scrape() instead of scrape_url()
    # Returns a Document object with .markdown and .metadata attributes
    scrapeResult = app.scrape(input['url'])

    content = scrapeResult.markdown
    metadata = scrapeResult.metadata
    title = 'Untitled Article'
    
    if metadata:
        # metadata can be accessed as dict or object depending on version
        if hasattr(metadata, 'get'):
            title = metadata.get('title', 'Untitled Article')
        elif hasattr(metadata, 'title'):
            title = metadata.title or 'Untitled Article'

    context.logger.info(f"✅ Successfully scraped: {title} ({len(content) if content else 0} characters)")

    await context.emit({
        'topic': 'generate-content',
        'data': {
            'requestId': input['requestId'],
            'url': input['url'],
            'title': title,
            'content': content,
            'timestamp': input['timestamp']
        }
    })
