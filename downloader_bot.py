import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a YouTube, Instagram, or Twitter video link to download.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'cookiefile': 'cookies.txt',  # 👈 Use login cookies to bypass restrictions
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            await update.message.reply_video(video=open(file_path, 'rb'))
            os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

if __name__ == '__main__':
    os.makedirs("downloads", exist_ok=True)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("🤖 Bot is running...")
    app.run_polling()
