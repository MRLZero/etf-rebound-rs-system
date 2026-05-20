# coding=utf-8
from config import ETFS
from market import get_market_regime
from etf_analyzer import analyze
from notifier import send_tg

def main():
    market = get_market_regime()

    msg = "📈 *ETF RS Rebound Signals*\n\n"
    msg += (
        f"🌎 Market Regime:\n"
        f"VOO > MA200: {'✅' if market['voo_bull'] else '❌'}\n"
        f"QQQ > MA200: {'✅' if market['qqq_bull'] else '❌'}\n\n"
    )

    found = False

    for symbol, item in ETFS.items():
        try:
            window, category = item.get("window", 180), item.get("category", "Unknown")
            result = analyze(symbol, window, market)
            if result:
                found = True
                # category = symbol in ETFS and ETFS[symbol] or "Unknown"
                msg += (
                    f"{result['symbol']} {category}\n"
                    f"Price: ${result['price']}\n"
                    f"Recent High: ${result['high']}\n"
                    f"Recent Low: ${result['low']}\n"
                    f"Drawdown: {result['drawdown']}%\n"
                    f"Rebound: +{result['rebound']}%\n"
                    # f"RS Ratio: {result['rs']}\n"
                    f"Window: {result['window']}\n"
                    f"{result['state']} \n\n"
                )
        except Exception as e:
            print(f"{symbol} error: {e}")

    if not found:
        msg += "No strong RS rebound setup today."

    print(msg)
    send_tg(msg)


if __name__ == "__main__":
    main()