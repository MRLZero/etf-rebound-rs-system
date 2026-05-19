# coding=utf-8

# import yfinance as yf
import akshare as ak


def get_market_regime():
    """获取市场牛熊状态"""
    # voo = yf.download("SPY", period="1y", auto_adjust=True)
    # qqq = yf.download("QQQ", period="1y", auto_adjust=True)

    voo = ak.stock_us_daily(symbol="VOO", adjust='qfq')
    qqq = ak.stock_us_daily(symbol="QQQ", adjust='qfq')


    voo_close = voo["close"]
    qqq_close = qqq["close"]

    voo_now = float(voo_close.iloc[-1])
    qqq_now = float(qqq_close.iloc[-1])

    voo_ma200 = float(voo_close.rolling(200).mean().iloc[-1])
    qqq_ma200 = float(qqq_close.rolling(200).mean().iloc[-1])

    voo_bull = voo_now > voo_ma200
    qqq_bull = qqq_now > qqq_ma200
    bull_market = voo_bull and qqq_bull

    return {
        "voo_bull": voo_bull,
        "qqq_bull": qqq_bull,
        "bull_market": bull_market,
        "voo_close": round(voo_now, 2),
        "voo_ma200": round(voo_ma200, 2),
        "qqq_close": round(qqq_now, 2),
        "qqq_ma200": round(qqq_ma200, 2)
    }