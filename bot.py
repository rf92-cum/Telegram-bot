import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_FILE = "video.mp4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gunakan:\n/dl <link video>")

async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan: /dl <url>")
        return

    url = context.args[0]
    await update.message.reply_text("Downloading...")

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": DOWNLOAD_FILE,
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(DOWNLOAD_FILE):
            with open(DOWNLOAD_FILE, "rb") as vid:
                await update.message.reply_video(video=vid)

            os.remove(DOWNLOAD_FILE)
        else:
            await update.message.reply_text("Download gagal.")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("dl", dl))

print("BOT RUNNING...")
app.run_polling()
