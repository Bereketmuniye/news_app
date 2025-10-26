# Centralized sources: RSS for news/social/other. No keys!
# Twitter: Via RSS.app (free RSS from Twitter users/searches)
# Reddit: Native RSS
# Format: {country: {source_type: {category: 'url'}}}

sources = {
    'us': {
        'web': {  # CNN RSS
            'general': 'http://rss.cnn.com/rss/cnn_topstories.rss',
            'technology': 'http://rss.cnn.com/rss/edition_technology.rss',
            'sports': 'http://rss.cnn.com/rss/cnn_sport.rss',
            'business': 'http://rss.cnn.com/rss/money_latest.rss',
            'health': 'http://rss.cnn.com/rss/cnn_health.rss',
        },
        'twitter': {  # RSS.app for Twitter (e.g., @CNN, search "news")
            'general': 'https://rss.app/feeds/twitter/CNN.xml',  # CNN Twitter
            'technology': 'https://rss.app/feeds/twitter/search.xml?q=technology%20news',  # Search
            'sports': 'https://rss.app/feeds/twitter/ESPN.xml',
            'business': 'https://rss.app/feeds/twitter/search.xml?q=business%20news',
            'health': 'https://rss.app/feeds/twitter/search.xml?q=health%20news',
        },
        'reddit': {  # r/ subreddits
            'general': 'https://www.reddit.com/r/news/.rss',
            'technology': 'https://www.reddit.com/r/technology/.rss',
            'sports': 'https://www.reddit.com/r/sports/.rss',
            'business': 'https://www.reddit.com/r/business/.rss',
            'health': 'https://www.reddit.com/r/health/.rss',
        }
    },
    'uk': {
        'web': {  # BBC RSS
            'general': 'http://feeds.bbci.co.uk/news/rss.xml',
            'technology': 'http://feeds.bbci.co.uk/news/technology/rss.xml',
            'sports': 'http://feeds.bbci.co.uk/sport/rss.xml',
            'business': 'http://feeds.bbci.co.uk/news/business/rss.xml',
            'health': 'http://feeds.bbci.co.uk/news/health/rss.xml',
        },
        'twitter': {
            'general': 'https://rss.app/feeds/twitter/BBCBreaking.xml',
            'technology': 'https://rss.app/feeds/twitter/search.xml?q=technology%20uk',
            'sports': 'https://rss.app/feeds/twitter/BBC_Sport.xml',
            'business': 'https://rss.app/feeds/twitter/search.xml?q=business%20uk',
            'health': 'https://rss.app/feeds/twitter/search.xml?q=health%20uk',
        },
        'reddit': {  # Same as US (global subs)
            'general': 'https://www.reddit.com/r/news/.rss',
            'technology': 'https://www.reddit.com/r/technology/.rss',
            'sports': 'https://www.reddit.com/r/sports/.rss',
            'business': 'https://www.reddit.com/r/business/.rss',
            'health': 'https://www.reddit.com/r/health/.rss',
        }
    },
    'et': {  # NEW: Ethiopia (YouTube focus + basic Web)
        'web': {  # Addis Standard RSS (English/Amharic news)
            'general': 'https://addisstandard.com/feed/',  
        },
        'youtube': {  # EBC (official broadcaster)
            'general': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCOhrz3uRCOHmK6ueUstw7_Q',  # EBC
        },
        'twitter': {
            'general': 'https://rss.app/feeds/twitter/search.xml?q=Ethiopia%20news',  # Search-based
        },
        'reddit': {
            'general': 'https://www.reddit.com/r/Ethiopia/.rss',  # r/Ethiopia
        }
    }
}