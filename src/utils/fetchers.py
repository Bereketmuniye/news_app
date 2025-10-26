import feedparser
import requests
import logging
from typing import List, Optional, Dict
from src.config.sources import sources

logger = logging.getLogger(__name__)

def fetch_rss(url: str) -> Optional[List[Dict[str, str]]]:
    """Fetches RSS, returns list of {'title': str, 'link': str, 'image': str or None} or None."""
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            articles = []
            for entry in feed.entries[:20]:
                title = entry.get('title', 'No title')
                link = entry.get('link', '')
                image = None
                if hasattr(entry, 'media_thumbnail'):
                    image = entry.media_thumbnail[0]['url'] if entry.media_thumbnail else None
                elif entry.enclosures:
                    enc = next((e for e in entry.enclosures if e.type.startswith('image/')), None)
                    if enc:
                        image = enc.href
                articles.append({'title': title, 'link': link, 'image': image})
            return articles
        return None
    except Exception as e:
        logger.error(f"RSS error: {e}")
        return None

def fetch_weather(city: str) -> Optional[str]:
    """Fetches detailed weather via wttr.in (humidity, wind, etc.)."""
    try:
        url = f"http://wttr.in/{city}?format=%l:+%c+%t+%w+%h+%p+%f+%u"
        response = requests.get(url, timeout=10) 
        response.raise_for_status()
        weather_text = response.text.strip()
        if weather_text:
            weather_text = weather_text.replace('+', ' | ')
            return weather_text
        return None
    except Exception as e:
        logger.error(f"Weather error for {city}: {e}")
        return None