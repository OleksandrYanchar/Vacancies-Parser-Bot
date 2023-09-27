import asyncio
from celery import Celery
import schedule
from src.bot.bot import bot_schedule

"""
Starts schedule task which starts polling bot at specified time and 
then stops it
"""
#Creates celery app
app = Celery('my_schedule', broker='pyamqp://guest@localhost//')

#defines celey task
@app.task
def run_my_script():
    asyncio.run(bot_schedule())

#setups schedule for task 
schedule.every().day.at("05:30").do(run_my_script)

#runs task use command celery -A my_schedule  worker --loglevel=info
while True:
    schedule.run_pending()
