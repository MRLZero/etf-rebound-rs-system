# coding=utf-8

# import yfinance as yf
import akshare as ak


def get_market_regime():
    """获取市场牛熊状态"""
    # spy = yf.download("SPY", period="1y", auto_adjust=True)
    # qqq = yf.download("QQQ", period="1y", auto_adjust=True)

    spy = ak.stock_us_daily(symbol="SPY", adjust='qfq')
    qqq = ak.stock_us_daily(symbol="QQQ", adjust='qfq')


    spy_close = spy["close"]
    qqq_close = qqq["close"]

    spy_now = float(spy_close.iloc[-1])
    qqq_now = float(qqq_close.iloc[-1])

    spy_ma200 = float(spy_close.rolling(200).mean().iloc[-1])
    qqq_ma200 = float(qqq_close.rolling(200).mean().iloc[-1])

    spy_bull = spy_now > spy_ma200
    qqq_bull = qqq_now > qqq_ma200
    bull_market = spy_bull and qqq_bull

    return {
        "spy_bull": spy_bull,
        "qqq_bull": qqq_bull,
        "bull_market": bull_market,
        "spy_close": round(spy_now, 2),
        "spy_ma200": round(spy_ma200, 2),
        "qqq_close": round(qqq_now, 2),
        "qqq_ma200": round(qqq_ma200, 2)
    }