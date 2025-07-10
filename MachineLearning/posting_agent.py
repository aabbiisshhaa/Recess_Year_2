import logging
import random
import asyncio
import nest_asyncio
import pytz

from datetime import datetime, time, timedelta
from telegram.ext import ( Application, CommandHandler, ContextTypes, )

# Define timezone (change 'Africa/Kampala' if you're in a different region)
UGANDA_TZ = pytz.timezone('Africa/Kampala')

# Configuration
CHANNEL_CHAT_ID = -1002768097716
BOT_TOKEN = "8049052561:AAFOORt1IUWAcJ5wrtIzjaJ6xZTZykPdmSI"

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Message Pools 
MORNING_QUIZZES = [
    "What does HTML stand for?",
    "What is the purpose of the <head> tag in HTML?",
    "Which language is used for styling web pages?",
    "What does CSS stand for?",
    "What does JS stand for in web development?"
]


AFTERNOON_FACTS = [
    "The first computer bug was an actual moth.",
    "The first 1GB hard drive was the size of a fridge.",
    "Email existed before the world wide web.",
    "The first computer programmer was Ada Lovelace.",
    "The first domain name ever registered was symbolics.com."
]


EVENING_POLLS = [
    "How many hours do you spend on tech daily?",
    "Do you prefer dark mode or light mode?",
    "What's your favorite programming language?",
    "How often do you update your software?",
    "Do you use AI tools in your daily workflow?"
]


# Scheduled Tasks 
async def morning_quiz(context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(MORNING_QUIZZES)
    await context.bot.send_message(chat_id=CHANNEL_CHAT_ID, text=f"🌞 Daily Quiz:\n\n{msg}")
    logger.info("Morning quiz sent.")

async def afternoon_fact(context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(AFTERNOON_FACTS)
    await context.bot.send_message(chat_id=CHANNEL_CHAT_ID, text=f"📘 Tech Fact:\n\n{msg}")
    logger.info("Afternoon fact sent.")

async def evening_poll(context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(EVENING_POLLS)
    await context.bot.send_message(chat_id=CHANNEL_CHAT_ID, text=f"🌙 Evening Poll:\n\n{msg}")
    logger.info("Evening poll sent.")

# Command Handler 
async def start_command(update, context):
    await update.message.reply_text("Bot is running!")
    logger.info("/start command received.")

# Job Setup (recurring daily)
def setup_jobs(app):
    job_queue = app.job_queue
    
    # Schedule jobs to run at specific times
    morning_time = time(hour=8, minute=0, tzinfo=UGANDA_TZ)
    afternoon_time = time(hour=12, minute=41, tzinfo=UGANDA_TZ)
    evening_time = time(hour=18, minute=0, tzinfo=UGANDA_TZ)
    
    logger.info("Scheduling daily jobs...")
    job_queue.run_daily(morning_quiz, time=morning_time, days=(0, 1, 2, 3, 4, 5, 6))
    job_queue.run_daily(afternoon_fact, time=afternoon_time, days=(0, 1, 2, 3, 4, 5, 6))
    job_queue.run_daily(evening_poll, time=evening_time, days=(0, 1, 2, 3, 4, 5, 6))
    
    # Schedule jobs to run once at specific intervals for testing   
    # logger.info("Scheduling job to run in 10, 20 and 30 seconds...")
    
    # job_queue.run_once(morning_quiz, when=timedelta(seconds=10))
    # job_queue.run_once(afternoon_fact, when=timedelta(seconds=20))
    # job_queue.run_once(evening_poll, when=timedelta(seconds=30))
    
    
# Main Function 
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    setup_jobs(app)

    logger.info("Starting bot...")
    await app.run_polling()

# === Script Entry Point ===
if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()  # Allow reuse of the already-running event loop
    asyncio.get_event_loop().run_until_complete(main())
