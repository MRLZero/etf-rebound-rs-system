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