from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.config.sources import sources
from src.utils.fetchers import fetch_rss
import os
from dotenv import load_dotenv

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome + country select (added Ethiopia)."""
    text = "👋 News & Weather Bot! Pick country:"
    keyboard = [
        [InlineKeyboardButton("🇺🇸 US", callback_data='country_us')],
        [InlineKeyboardButton("🇬🇧 UK", callback_data='country_uk')],
        [InlineKeyboardButton("🇪🇹 Ethiopia", callback_data='country_et')],  # NEW
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """General news (default to web) with photos/links."""
    user_data = context.user_data
    if 'country' not in user_data:
        await update.message.reply_text("Pick country with /start! 🌍")
        return
    country = user_data['country']
    await update.message.reply_text("Fetching general web news... ⏳")
    # Fallback if no web for country (e.g., et uses general)
    web_sources = sources.get(country, {}).get('web', {})
    url = web_sources.get('general', sources['us']['web']['general'])  # Default to US if missing
    articles = fetch_rss(url)
    if articles:
        for article in articles:
            title = article['title']
            link = article['link']
            image = article['image']
            caption = f"**{title}**\n\n[Read more]({link})"
            if image:
                await update.message.reply_photo(photo=image, caption=caption, parse_mode='Markdown')
            else:
                text = f"📰 **{title}**\n\n[Read more]({link})"
                await update.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("No news found. 😔")

# Message handler for city input (weather)
async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Triggered after weather button; fetch for city."""
    city = update.message.text.strip()
    user_data = context.user_data
    if 'country' not in user_data:
        await update.message.reply_text("Pick country first! /start")
        return
    from src.utils.fetchers import fetch_weather
    weather = fetch_weather(city)
    if weather:
        country_name = {'us': 'US', 'uk': 'UK', 'et': 'Ethiopia'}.get(user_data['country'], user_data['country'].upper())
        await update.message.reply_text(f"🌤️ **Weather in {city} ({country_name})**\n\n{weather}")
    else:
        await update.message.reply_text(f"Couldn't get weather for {city}. Try another city! (e.g., Addis Ababa)")
    # Reset for next use
    context.user_data.pop('waiting_for_city', None)