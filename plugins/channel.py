async def send_movie_updates(bot, file_name, file_id):
    imdb_title, poster_url, caption = await get_imdb(file_name)
    
    if not imdb_title or imdb_title in processed_movies:
        return  
    
    processed_movies.add(imdb_title)
    
    if not poster_url or not caption:
        return  

    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', name_format(file_name)).strip().replace(" ", "-")

    btn = [[InlineKeyboardButton('📂 Get Files Bot', url=f'https://telegram.me/AllMoviesRobot?start=getfile-{clean_title}')]]
    reply_markup = InlineKeyboardMarkup(btn)
    movie_update_channel = await db.movies_update_channel_id()

    try:
        await bot.send_photo(
            movie_update_channel if movie_update_channel else MOVIE_UPDATE_CHANNEL,
            photo=poster_url,
            caption=caption,
            reply_markup=reply_markup
        )
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"Failed to send movie update. Error - {error_message}")
        await bot.send_message(LOG_CHANNEL, f"Failed to send movie update. Error - <code>{error_message}</code>")
