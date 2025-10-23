import os
from fastapi import FastAPI, Request
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

app = FastAPI()
tg_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def start(update, context):
    await update.message.reply_text("ربات فعاله. پیام بده.")

async def chat(update, context):
    user_text = update.message.text or ""
    if not user_text.strip():
        await update.message.reply_text("لطفا پیام متنی بفرست.")
        return

    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.responses.create(
            model="gpt-4o-mini",
            input=f"Answer in Persian. User said: {user_text}"
        )
        answer = resp.output_text if hasattr(resp, "output_text") else "خطا در پاسخ."
    else:
        answer = "کلید OpenAI تنظیم نشده."

    await update.message.reply_text(answer)

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}
