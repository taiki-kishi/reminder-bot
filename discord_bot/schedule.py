import requests
from .config import (
    WEBHOOK_HITOKU, WEBHOOK_FTQC, WEBHOOK_NEDO,
    WEBHOOK_MED, WEBHOOK_QI, WEBHOOK_LAB,
    MENTION_HITOKU, MENTION_FTQC, MENTION_NEDO,
    MENTION_MED, MENTION_QI, MENTION_LAB
)

# ===== メッセージテンプレ =====

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
    if not url:
        print("[WARN] Webhook URL not set, skipping")
        return
    requests.post(
        url,
        json={
            "content": msg,
            "allowed_mentions": {
                "parse": ["roles", "users", "everyone"]
            }
        },
        timeout=10,
    )

# ===== 曜日ごとの実行 =====
# Mon=0 Tue=1 Wed=2 Thu=3 Fri=4

def run_for_today(weekday: int):

    # 月：火曜ミート reminder（秘匿・FTQC）
    if weekday == 0:
        send_webhook(WEBHOOK_HITOKU, template_reminder(MENTION_HITOKU))
        send_webhook(WEBHOOK_FTQC,   template_reminder(MENTION_FTQC))

    # 火：after（秘匿・FTQC）
    elif weekday == 1:
        send_webhook(WEBHOOK_HITOKU, template_after(MENTION_HITOKU))
        send_webhook(WEBHOOK_FTQC,   template_after(MENTION_FTQC))

    # 水：木曜ミート reminder（NEDO）
    elif weekday == 2:
        send_webhook(WEBHOOK_NEDO, template_reminder(MENTION_NEDO))

    # 木：after（NEDO）＋金曜 reminder（医療・QI）＋研究室全体
    elif weekday == 3:
        send_webhook(WEBHOOK_NEDO, template_after(MENTION_NEDO))
        send_webhook(WEBHOOK_MED,  template_reminder(MENTION_MED))
        send_webhook(WEBHOOK_QI,   template_reminder(MENTION_QI))
        send_webhook(WEBHOOK_LAB,  template_lab_meeting(MENTION_LAB))

    # 金：after（医療・QI）
    elif weekday == 4:
        send_webhook(WEBHOOK_MED, template_after(MENTION_MED))
        send_webhook(WEBHOOK_QI,  template_after(MENTION_QI))

    else:
        print("[INFO] Weekend: nothing to send")

