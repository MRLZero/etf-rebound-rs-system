# coding=utf-8
import os
import requests

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")


def send_tg(msg):
    """发送Telegram消息"""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(
        url,
        json={
            "chat_id": TG_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }
    )


from math import ceil


# -----------------------------
# 估值字段格式化
# -----------------------------
def _fmt_valuation(result: dict) -> str:
    """PE 格式化：PE: 28.5 或 PE: N/A"""
    pe_cur = result.get("pe_current")
    return f"PE: {pe_cur}" if pe_cur is not None else "PE: N/A"


def build_messages(results, max_items=15):

    # -----------------------------
    # 过滤 None
    # -----------------------------
    filtered = [
        r for r in results
        if r is not None
    ]

    # -----------------------------
    # 信号优先级
    # -----------------------------
    priority = {
        "🚀 STRONG BUY": 1,
        "🚀 BUY": 2,
        "⚪ WATCH": 3,
        "⚪ No-Trade": 4
    }

    # -----------------------------
    # 排序
    # 1. signal
    # 2. recovery_ratio
    # -----------------------------
    filtered.sort(
        key=lambda x: (
            priority.get(x["state"], 99),
            x["recovery_ratio"]
        )
    )

    # -----------------------------
    # 拆分消息
    # -----------------------------
    total_msgs = ceil(
        len(filtered) / max_items
    )

    messages = []

    for i in range(total_msgs):

        chunk = filtered[
            i * max_items:
            (i + 1) * max_items
        ]

        msg = (
            f"📊 ETF/Stock Quant Signals "
            f"({i+1}/{total_msgs})\n\n"
        )

        current_signal = None

        for result in chunk:

            # -----------------------------
            # 新 signal section
            # -----------------------------
            if result["state"] != current_signal:
                current_signal = result["state"]
                msg += f"\n{current_signal}\n\n"

            # -----------------------------
            # 估值行
            # -----------------------------
            valuation_line = _fmt_valuation(result)

            # -----------------------------
            # 行内容
            # -----------------------------
            line = (
                f"{result['symbol']} {result['category']}\n"
                f"Price: ${result['price']}\n"
                f"Recent High: ${result['high']}\n"
                f"Recent Low: ${result['low']}\n"
                f"cDrawdown: {result['drawdown']}%\n"
                f"cRebound: +{result['rebound']}%\n"
                f"Recovery Ratio: {result['recovery_ratio']}\n"
                f"pDrawdown: {result['pre_drawdown']}%\n"
                f"{valuation_line}\n"
                f"Window: {result['window']}\n\n"
            )

            msg += line

        messages.append(msg)

    return messages


# -----------------------------
# Send Telegram Messages
# -----------------------------
def send_telegram_messages(results):
    """Telegram 推送"""

    try:
        messages = build_messages(results)
        for msg in messages:
            send_tg(msg)
            print(msg)

        print(
            f"Telegram sent: "
            f"{len(messages)} messages"
        )

    except Exception:
        print("Telegram send error")


if __name__ == '__main__':
    msg = "Hello!"
    send_tg(msg)
