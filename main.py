import asyncio
from src.configs.settings import TOKEN

if __name__=='__main__':
    from src.bot.bot import main
    asyncio.run(main())

