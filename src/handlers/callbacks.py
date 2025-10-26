from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.config.sources import sources
from src.utils.fetchers import fetch_rss

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flow: country > weather/news > source > cat > fetch & send with photos/highlights."""
    query = update.callback_query
    await query.answer()
    data = query.data
    user_data = context.user_data

    if data.startswith('country_'):
        country = data.split('_')[1]
        user_data['country'] = country
        text = f"Selected {country.upper()}! What next?"
        keyboard = [
            [InlineKeyboardButton("🌤️ Weather", callback_data=f'weather_{country}')],
            [InlineKeyboardButton("📰 News Sources", callback_data=f'news_{country}')],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith('weather_'):
        # Ask for city
        user_data['waiting_for_city'] = True
        country_name = {'us': 'US', 'uk': 'UK', 'et': 'Ethiopia'}[data.split('_')[1]]
        await query.edit_message_text(f"Enter city name for {country_name} (e.g., Addis Ababa):")

    elif data.startswith('news_'):
        # News sources
        country = data.split('_')[1]
        text = "Pick news source:"
        keyboard = [
            [InlineKeyboardButton("🌐 Web Sites", callback_data=f'source_web_{country}')],
            [InlineKeyboardButton("🐦 Twitter/X", callback_data=f'source_twitter_{country}')],
            [InlineKeyboardButton("🔴 Reddit", callback_data=f'source_reddit_{country}')],
        ]
        # Add YouTube for all countries
        keyboard.append([InlineKeyboardButton("📺 YouTube Videos", callback_data=f'source_youtube_{country}')])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith('source_'):
        # Source > Categories (for YouTube: no cats, fetch direct)
        parts = data.split('_')
        source_type = parts[1]
        country = parts[2]
        user_data['source'] = source_type
        if source_type == 'youtube':
            # Direct fetch for YouTube (main channel)
            await query.edit_message_text("Fetching latest YouTube videos... ⏳")
            yt_sources = sources.get(country, {}).get('youtube', {})
            url = yt_sources.get('general', '')  # Fallback empty
            if not url:
                await query.edit_message_text("YouTube not available for this country yet. Try Web! 😔")
                return
            articles = fetch_rss(url)
            emoji = "📺"
            source_display = "YouTube"
            cat_display = "Latest Videos"
            if articles:
                for article in articles:
                    title = article['title']
                    link = article['link']
                    image = article['image']
                    caption = f"**{title}**\n\n[Watch now]({link})"
                    if image:
                        await query.message.reply_photo(photo=image, caption=caption, parse_mode='Markdown')
                    else:
                        text = f"{emoji} **{title}**\n\n[Watch now]({link})"
                        await query.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True)
                await query.edit_message_text(f"✅ Sent {len(articles)} {cat_display} from {source_display}!")
            else:
                await query.edit_message_text(f"No {cat_display} from {source_display}. 😔")
        else:
            # Other sources: Show categories
            text = "Pick category:"
            keyboard = [
                [InlineKeyboardButton("💻 Technology", callback_data=f'cat_technology_{country}_{source_type}')],
                [InlineKeyboardButton("⚽ Sports", callback_data=f'cat_sports_{country}_{source_type}')],
                [InlineKeyboardButton("💼 Business", callback_data=f'cat_business_{country}_{source_type}')],
                [InlineKeyboardButton("🏥 Health", callback_data=f'cat_health_{country}_{source_type}')],
                [InlineKeyboardButton("🏠 General", callback_data=f'cat_general_{country}_{source_type}')],
            ]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith('cat_'):
        # Fetch & send enhanced messages (same as before)
        parts = data.split('_', 2)
        category = parts[1]
        country_source = parts[2]  # e.g., 'us_web'
        country, source_type = country_source.split('_')
        
        await query.edit_message_text(f"Fetching {category} from {source_type}... ⏳")
        
        url_dict = sources.get(country, {}).get(source_type, {})
        url = url_dict.get(category, url_dict.get('general', ''))
        if not url:
            await query.edit_message_text("Source not available for this category/country. Try another! 😔")
            return
        articles = fetch_rss(url)
        
        source_display = {'web': 'Web', 'twitter': 'Twitter', 'reddit': 'Reddit'}[source_type]
        cat_display = "General" if category == 'general' else category.title()
        emoji = {'web': '📰', 'twitter': '🐦', 'reddit': '🔴'}[source_type]
        
        if articles:
            for article in articles:
                title = article['title']
                link = article['link']
                image = article['image']
                
                # Highlighted caption: **Title** \n [Read more](link)
                caption = f"**{title}**\n\n[Read more]({link})"
                
                if image:
                    # Send photo with caption
                    await query.message.reply_photo(
                        photo=image,
                        caption=caption,
                        parse_mode='Markdown'
                    )
                else:
                    # Fallback: Text message
                    text = f"{emoji} **{title}**\n\n[Read more]({link})"
                    await query.message.reply_text(
                        text,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
            # Edit original to summary
            await query.edit_message_text(f"✅ Sent {len(articles)} {cat_display} {source_display} items with photos/links!")
        else:
            await query.edit_message_text(f"No {cat_display} {source_display} news. Try another! 😔")