import feedparser
from app.config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RSSCollector:
    @staticmethod
    def collect_feeds():
        articles = []
        
        for feed_url in settings.feeds_list:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:
                    article = {
                        "feed_source": feed_url,
                        "title": entry.get("title", ""),
                        "content": entry.get("summary", entry.get("description", "")),
                        "link": entry.get("link", ""),
                        "published_date": datetime.now(),
                        "raw_data": str(entry),
                    }
                    articles.append(article)
            except Exception as e:
                logger.error(f"Error parsing feed {feed_url}: {str(e)}")
        
        return articles
