# coding=utf-8
from config import ETFS
from market import get_market_regime
from etf_analyzer import analyze
from notifier import send_tg, send_telegram_messages


def main():
    results = []
    market = get_market_regime()

    # msg = "📈 *ETF RS Rebound Signals*\n\n"
    msg = (
        f"🌎 Market Regime:\n\n"
        f"VOO > MA200: {'✅' if market['voo_bull'] else '❌'}\n"
        f"QQQ > MA200: {'✅' if market['qqq_bull'] else '❌'}\n\n"
    )
    send_tg(msg)

    for symbol, item in ETFS.items():
        try:
            window, category = item.get("window", 180), item.get("category", "Unknown")
            result = analyze(symbol, window, market)
            if result:
                result["category"] = category
                results.append(result)

        except Exception as e:
            print(f"{symbol} error: {e}")

    send_telegram_messages(results)

if __name__ == "__main__":
    main()