from aiogram.utils import executor
from init_bot import dp
from handlers import client

async def on_startup(_):
    print("Bot successfully started!")
client.register_handlers(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
#executor.start_webhook(dp,skip_updates=True,on_startup=on_startup)