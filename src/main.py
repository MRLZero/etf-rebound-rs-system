# coding=utf-8

from config import ETFS, BENCHMARK
from market import get_market_regime
from etf_analyzer import analyze, fetch_etf_history
from notifier import send_tg, send_telegram_messages


def main():

    results = []

    # ---------------------------------
    # 市场环境
    # ---------------------------------
    market = get_market_regime()

    # ---------------------------------
    # 下载基准ETF（仅一次）
    # ---------------------------------
    print(f"Loading benchmark: {BENCHMARK}")

    benchmark_data = fetch_etf_history(BENCHMARK)

    if benchmark_data is None or benchmark_data.empty:

        error_msg = (
            f"❌ Benchmark download failed:\n"
            f"{BENCHMARK}"
        )

        print(error_msg)

        send_tg(error_msg)

        return

    # ---------------------------------
    # 市场状态推送
    # ---------------------------------
    msg = (
        f"🌎 Market Regime\n\n"
        f"Benchmark: {BENCHMARK}\n\n"
        f"VOO > MA200: {'✅' if market['voo_bull'] else '❌'}\n"
        f"QQQ > MA200: {'✅' if market['qqq_bull'] else '❌'}\n\n"
    )

    send_tg(msg)

    # ---------------------------------
    # ETF扫描
    # ---------------------------------
    total = len(ETFS)

    for idx, (symbol, item) in enumerate(
            ETFS.items(),
            start=1
    ):

        print(
            f"[{idx}/{total}] "
            f"Analyzing {symbol}"
        )

        try:

            window = item.get(
                "window",
                180
            )

            category = item.get(
                "category",
                "Unknown"
            )

            result = analyze(
                symbol=symbol,
                base_window=window,
                market=market,
                benchmark_data=benchmark_data
            )

            if result:

                result["category"] = category

                results.append(result)

        except Exception as e:

            print(
                f"{symbol} error: {e}"
            )

    # ---------------------------------
    # Telegram推送
    # ---------------------------------
    send_telegram_messages(results)


if __name__ == "__main__":
    main()