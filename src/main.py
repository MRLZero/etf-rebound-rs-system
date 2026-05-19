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
        f"SPY > MA200: {'✅' if market['spy_bull'] else '❌'}\n"
        f"QQQ > MA200: {'✅' if market['qqq_bull'] else '❌'}\n\n"
    )

    found = False

    for symbol, window in ETFS.items():
        try:
            result = analyze(symbol, window, market)
            if result:
                found = True
                msg += (
                    f"{result['symbol']}\n"
                    f"Price: ${result['price']}\n"
                    f"Recent High: ${result['high']}\n"
                    f"Recent Low: ${result['low']}\n"
                    f"Drawdown: {result['drawdown']}%\n"
                    f"Rebound: +{result['rebound']}%\n"
                    f"RS Ratio: {result['rs']}\n"
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