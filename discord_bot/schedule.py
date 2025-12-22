# schedule.py
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .config import *

scheduler = AsyncIOScheduler()

# ===== メッセージ =====

def template_reminder(mention):
    return f"""{mention}
明日は定例ミート予定日です
本日中にMarkdownの進捗を更新し、完了したら✅ を押してください
教員は進捗内容を確認したら🆗 を押してください
"""

def template_after(mention):
    return f"""{mention}
定例ミートおつかれさまでした
本日中にMarkdownの週次目標を更新し、完了したら✅を押してください
"""

def template_lab_meeting(mention):
    return f"""{mention}
明日は全体ミーティング予定日です
発表予定者は資料のアップロードが完了したら 🆗 を押してください
"""

# ===== Webhook送信 =====

def send_webhook(url, msg):
    requests.post(url, json={
        "content": msg,
        "allowed_mentions": {
            "parse": ["roles", "users", "everyone"]
        }
    })



def add(trigger, url, msg, job_id):
    scheduler.add_job(
        lambda: send_webhook(url, msg),
        trigger,
        id=job_id,
        replace_existing=True
    )


# ===== スケジュール設定 =====

def setup_schedules():

    # === 火曜ミート（秘匿・FTQC） ===
    # 月曜 17:30 reminder
    add(CronTrigger(day_of_week="mon", hour=17, minute=30),
        WEBHOOK_HITOKU, template_reminder(MENTION_HITOKU), "remind_hitoku_mon")
    add(CronTrigger(day_of_week="mon", hour=17, minute=30),
        WEBHOOK_FTQC, template_reminder(MENTION_FTQC), "remind_ftqc_mon")

    # 火曜 17:30 after
    add(CronTrigger(day_of_week="tue", hour=17, minute=30),
        WEBHOOK_HITOKU, template_after(MENTION_HITOKU), "after_hitoku_tue")
    add(CronTrigger(day_of_week="tue", hour=17, minute=30),
        WEBHOOK_FTQC, template_after(MENTION_FTQC), "after_ftqc_tue")


    # === 木曜ミート（NEDO） ===
    add(CronTrigger(day_of_week="wed", hour=17, minute=30),
        WEBHOOK_NEDO, template_reminder(MENTION_NEDO), "remind_nedo_wed")
    add(CronTrigger(day_of_week="thu", hour=17, minute=30),
        WEBHOOK_NEDO, template_after(MENTION_NEDO), "after_nedo_thu")


    # === 金曜ミート（医療QML・QI） ===
    # 木曜 reminder
    add(CronTrigger(day_of_week="thu", hour=17, minute=30),
        WEBHOOK_MED, template_reminder(MENTION_MED), "remind_med_thu")
    add(CronTrigger(day_of_week="thu", hour=17, minute=30),
        WEBHOOK_QI, template_reminder(MENTION_QI), "remind_qi_thu")

    # 金曜 after
    add(CronTrigger(day_of_week="fri", hour=17, minute=30),
        WEBHOOK_MED, template_after(MENTION_MED), "after_med_fri")
    add(CronTrigger(day_of_week="fri", hour=17, minute=30),
        WEBHOOK_QI, template_after(MENTION_QI), "after_qi_fri")


    # === 研究室全体ミーティング（木曜 17:30 前日リマインダ） ===
    add(CronTrigger(day_of_week="thu", hour=17, minute=30),
        WEBHOOK_LAB, template_lab_meeting(MENTION_LAB), "remind_lab_thu")

    scheduler.start()
