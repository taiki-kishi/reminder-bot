import asyncio
from .schedule import setup_schedules

async def main():
    print("Discord Webhook Meeting Reminder Bot Started")
    setup_schedules()

    # asyncio が止まらないようにループ
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
