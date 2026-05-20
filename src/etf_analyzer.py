# coding=utf-8
# import yfinance as yf
import akshare as ak

import pandas as pd
import numpy as np
from config import MA_SHORT, MA_MID, MA_LONG, SIGNAL_THRESHOLDS, VOLUME_SURGE_FACTOR, RS_BREAKOUT_FACTOR

# -----------------------------
# 动态 window 计算函数
# -----------------------------
def get_dynamic_window(close, base_window=120, min_window=60, max_window=180):
    """
    根据波动率动态调整 window
    高波动 -> window 小，低波动 -> window 大
    """
    vol = close.pct_change().rolling(20).std().iloc[-1]
    if np.isnan(vol) or vol == 0:
        return base_window
    vol_factor = vol / 0.025  # 0.02 为参考基准，可调整
    window = int(base_window / vol_factor)
    window = max(min_window, min(max_window, window))
    return window

# -----------------------------
# 连续上涨天数函数
# -----------------------------
def consecutive_up_days(close, n=3):
    if len(close) < n+1:
        return False
    return (close[-n:].values > close[-n-1:-1].values).all()

# -----------------------------
# ETF 分析函数
# -----------------------------
def fetch_etf_history(symbol, period_days=365):
    """
    获取 ETF 历史行情，并统一截取最近 period_days 的数据

    symbol: str, ETF 代码，如 '510300'（沪深300 ETF）
    period_days: int, 最近多少天数据
    """
    try:
        # 获取 ETF 日线行情
        # akshare 里沪深ETF一般使用 ak.fund_etf_daily
        # df = ak.fund_etf_daily(symbol)
        df = ak.stock_us_daily(symbol=symbol, adjust='qfq')
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

    if df.empty:
        return None

    # df 默认列名：date, open, high, low, close, volume, amount
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')  # 按时间升序排序

    # 获取最近 period_days 的数据
    end_date = df['date'].max()
    start_date = end_date - pd.Timedelta(days=period_days)
    df_filtered = df[df['date'] >= start_date].copy()

    df_filtered.reset_index(drop=True, inplace=True)
    return df_filtered

def analyze(symbol, base_window, market):
    """分析单只ETF信号"""
    try:
        # data = yf.download(symbol, period="1y", auto_adjust=True)
        # voo_data = yf.download("SPY", period="1y", auto_adjust=True)

        data = fetch_etf_history(symbol=symbol)
        voo_data = fetch_etf_history(symbol="VOO")

    except Exception as e:
        print(f"{symbol} download error: {e}")
        return None

    if data.empty or voo_data.empty:
        return None

    close = data["close"]
    volume = data["volume"]
    voo_close = voo_data["close"]

    # price = float(close.iloc[-1])

    # -----------------------------
    # 动态 window
    # -----------------------------
    window = get_dynamic_window(close, base_window)
    # 最近 window 数据
    recent_data = close.iloc[-window:]
    # 找最高点位置
    high_idx = recent_data.idxmax()
    recent_high = recent_data.loc[high_idx]
    # 只在 high 之后的数据里找低点
    after_high = recent_data.loc[high_idx:]
    recent_low = after_high.min()
    low_idx = after_high.idxmin()
    # 当前价格
    price = recent_data.iloc[-1]
    # 回撤
    drawdown = (price - recent_high) / recent_high * 100
    # 反弹
    rebound = (price - recent_low) / recent_low * 100
    # -----------------------------
    # 前期回撤过滤虚假反弹
    # -----------------------------
    pre_drawdown = (recent_high - recent_low) / recent_high * 100
    min_pre_drawdown = 10  # 最小回撤百分比，可调

    # -----------------------------
    # 均线趋势
    # -----------------------------
    ma_short = float(close.rolling(MA_SHORT).mean().iloc[-1])
    ma_mid = float(close.rolling(MA_MID).mean().iloc[-1])
    ma_long = float(close.rolling(MA_LONG).mean().iloc[-1])

    above_ma_short = price > ma_short
    strong_trend = ma_short > ma_mid
    healthy_long_term = price > ma_long * 0.9

    # -----------------------------
    # 成交量
    # -----------------------------
    latest_vol = float(volume.iloc[-1])
    vol20 = float(volume.rolling(20).mean().iloc[-1])
    volume_surge = latest_vol > vol20 * VOLUME_SURGE_FACTOR

    # -----------------------------
    # Relative Strength
    # -----------------------------
    rs_ratio = close / voo_close
    rs_now = float(rs_ratio.iloc[-1])
    rs_ma20 = float(rs_ratio.rolling(20).mean().iloc[-1])
    rs_ma50 = float(rs_ratio.rolling(50).mean().iloc[-1])
    rs_strong_short = rs_now >= rs_ma20
    rs_strong_mid = rs_now >= rs_ma50
    rs_high60 = float(rs_ratio.rolling(60).max().iloc[-1])
    rs_breakout = rs_now >= rs_high60 * RS_BREAKOUT_FACTOR

    bull_market = market["bull_market"]
    voo_bull = market["voo_bull"]



    # -----------------------------
    # 连续上涨天数
    # -----------------------------
    # up_days = consecutive_up_days(close, n=3)

    # -----------------------------
    # 信号判定
    # -----------------------------
    state = None

    if (
        drawdown <= SIGNAL_THRESHOLDS["STRONG_BUY"]["drawdown"]
        and rebound >= SIGNAL_THRESHOLDS["STRONG_BUY"]["rebound"]
        and strong_trend
        and volume_surge
        and healthy_long_term
        and rs_breakout
        and bull_market
        and pre_drawdown >= min_pre_drawdown
        # and up_days
    ):
        state = "🚀 STRONG BUY"

    elif (
        drawdown <= SIGNAL_THRESHOLDS["BUY"]["drawdown"]
        and rebound >= SIGNAL_THRESHOLDS["BUY"]["rebound"]
        and above_ma_short
        and strong_trend
        and rs_strong_mid
        and voo_bull
        and pre_drawdown >= min_pre_drawdown
        # and up_days
    ):
        state = "🚀 BUY"

    elif (
        drawdown <= SIGNAL_THRESHOLDS["WATCH"]["drawdown"]
        and rebound >= SIGNAL_THRESHOLDS["WATCH"]["rebound"]
        and above_ma_short
        and rs_strong_short
        # and up_days
    ):
        state = "⚪ WATCH"

    else:
        state = "⚪ No-Trade"

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "drawdown": round(drawdown, 1),
        "rebound": round(rebound, 1),
        "rs": round(rs_now, 3),
        "state": state,
        "high": round(recent_high, 2),
        "low": round(recent_low, 2),
        "window": window
    }