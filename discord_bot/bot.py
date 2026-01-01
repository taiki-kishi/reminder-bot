import datetime
from .config import (
    WEBHOOK_HITOKU,
    WEBHOOK_FTQC,
    WEBHOOK_NEDO,
    WEBHOOK_MED,
    WEBHOOK_QI,
    WEBHOOK_LAB,
)
import requests


def post(webhook_url: str, content: str):
    if not webhook_url:
        print("Webhook URL not set, skipping")
        return
    requests.post(webhook_url, json={"content": content})


def main():
    today = datetime.datetime.now(datetime.timezone.utc).astimezone(
        datetime.timezone(datetime.timedelta(hours=9))
    ).weekday()  

    print(f"Today weekday = {today}")

    # 月=0, 火=1, 水=2, 木=3, 金=4
    if today == 0:
        post(WEBHOOK_HITOKU, "【秘匿】定例ミーティングの時間です")
    elif today == 1:
        post(WEBHOOK_FTQC, "【FTQC】定例ミーティングの時間です")
    elif today == 2:
        post(WEBHOOK_NEDO, "【NEDO】定例ミーティングの時間です")
    elif today == 3:
        post(WEBHOOK_MED, "【医療】定例ミーティングの時間です")
    elif today == 4:
        post(WEBHOOK_QI, "【QI】定例ミーティングの時間です")

    # LAB は毎日
    post(WEBHOOK_LAB, "【研究室】進捗共有の時間です")

    print("Finished sending reminders")


if __name__ == "__main__":
    main()

