from datetime import datetime, timedelta, timezone
from .schedule import run_for_today


def main():
    # JST で曜日判定
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    weekday = now.weekday()  # Mon=0 ... Sun=6

    print(f"[INFO] JST now = {now.isoformat()}, weekday={weekday}")
    run_for_today(weekday)
    print("[INFO] Finished sending messages")


if __name__ == "__main__":
    main()

