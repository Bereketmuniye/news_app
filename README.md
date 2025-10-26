# Multi-Source News & Weather Bot

RSS-powered (Web/Twitter/Reddit) + wttr.in weather.

## Setup
1. `pip install -r requirements.txt`
2. Add BOT_TOKEN to .env
3. `python src/main.py`

## Flow
/start → Country → Weather (type city) or News → Source → Category
/news: Quick general web.

## Sources
- Web: CNN/BBC RSS
- Twitter: RSS.app (free)
- Reddit: Native RSS
- Weather: wttr.in (text)