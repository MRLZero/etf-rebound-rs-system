# coding=utf-8
import akshare as ak
import yfinance as yf

import pandas as pd
import numpy as np
from config import MA_SHORT, MA_MID, MA_LONG, SIGNAL_THRESHOLDS, VOLUME_SURGE_FACTOR, RS_BREAKOUT_FACTOR
from valuation import get_valuation

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
# 获取 ETF 历史行情
# -----------------------------
def fetch_etf_history(symbol):
    """
    获取美股 ETF / 个股历史行情（修复版：保留时间索引）

    核心变化：
    1. date 不再只是普通列 → 设为 index
    2. RS / benchmark 可安全按时间对齐
    3. 同时兼容 data["close"] 写法
    """

    try:
        df = yf.download(
            tickers=symbol,
            period="2y",
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=False,
            multi_level_index=False
        )

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

    if df is None or df.empty:
        print(f"{symbol}: empty dataframe")
        return None

    try:
        # -----------------------------
        # MultiIndex 兼容
        # -----------------------------
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # -----------------------------
        # index -> column
        # -----------------------------
        df = df.reset_index()

        rename_map = {
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }

        df.rename(columns=rename_map, inplace=True)

        required_cols = ["date", "open", "high", "low", "close", "volume"]

        if any(c not in df.columns for c in required_cols):
            print(f"{symbol}: missing columns")
            return None

        df = df[required_cols]

        # -----------------------------
        # 类型处理
        # -----------------------------
        df["date"] = pd.to_datetime(df["date"])

        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df.dropna(subset=["close"], inplace=True)

        df.sort_values("date", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # =============================
        # ⭐关键改动：保留 datetime index
        # =============================
        df.set_index("date", inplace=True)

        return df

    except Exception as e:
        print(f"{symbol} format error: {e}")
        return None

# -----------------------------
# ETF 分析函数
# -----------------------------
# def fetch_etf_history(symbol, period_days=365):
#     """
#     获取 ETF 历史行情，并统一截取最近 period_days 的数据
#
#     symbol: str, ETF 代码，如 '510300'（沪深300 ETF）
#     period_days: int, 最近多少天数据
#     """
#     try:
#         # 获取 ETF 日线行情
#         # akshare 里沪深ETF一般使用 ak.fund_etf_daily
#         # df = ak.fund_etf_daily(symbol)
#         df = ak.stock_us_daily(symbol=symbol, adjust='qfq')
#     except Exception as e:
#         print(f"Error fetching {symbol}: {e}")
#         return None
#
#     if df.empty:
#         return None
#
#     # df 默认列名：date, open, high, low, close, volume, amount
#     df['date'] = pd.to_datetime(df['date'])
#     df = df.sort_values('date')  # 按时间升序排序
#
#     # 获取最近 period_days 的数据
#     end_date = df['date'].max()
#     start_date = end_date - pd.Timedelta(days=period_days)
#     df_filtered = df[df['date'] >= start_date].copy()
#
#     df_filtered.reset_index(drop=True, inplace=True)
#     df_filtered.set_index("date", inplace=True)
#
#     return df_filtered

def confirm_volume_trend(volume, price=None,
                         short_window=5, long_window=20,
                         min_trend_strength=1.2,  # 短期均量 > 长期均量 * 1.2
                         require_price_up=True,  # 价格是否需同步上涨
                         volume_consistency=True,  # 要求量能平稳放大（避免单日跳变）
                         consistency_threshold=0.3  # 变异系数上限
                         ):
    """
    成交量趋势确认（代替原 volume_surge）

    Parameters
    ----------
    volume : pd.Series
        日成交量序列
    price : pd.Series, optional
        收盘价序列，用于价格-成交量一致性验证
    short_window : int
        短期均量窗口，默认5日
    long_window : int
        长期均量窗口，默认20日
    min_trend_strength : float
        短期均量 / 长期均量的最小倍数，默认1.2
    require_price_up : bool
        是否要求最新收盘价 > 昨日收盘价（上涨日）
    volume_consistency : bool
        是否要求量能平稳放大（防止单日巨量后缩量）
    consistency_threshold : float
        变异系数(CV)上限，超过则视为量能不平稳

    Returns
    -------
    bool
        是否满足成交量趋势确认条件
    dict
        详细指标（调试用）
    """
    if len(volume) < long_window + 1:
        return False, {}

    # 1. 计算短期和长期均量
    vol_short_ma = volume.rolling(short_window).mean()
    vol_long_ma = volume.rolling(long_window).mean()

    latest_vol_short = vol_short_ma.iloc[-1]
    latest_vol_long = vol_long_ma.iloc[-1]

    # 防止除零
    if latest_vol_long == 0:
        return False, {}

    # 2. 趋势强度判断
    trend_ratio = latest_vol_short / latest_vol_long
    trend_ok = trend_ratio >= min_trend_strength

    # 3. 量能趋势方向（最近短期均量是否上升）
    # 比较最近5日的短期均量斜率（简单线性回归或比较两端值）
    if len(vol_short_ma) >= 10:
        # 取最近10个值，计算回归斜率（正负判断）
        y = vol_short_ma.iloc[-10:].values
        x = np.arange(len(y))
        slope = np.polyfit(x, y, 1)[0]
        volume_increasing = slope > 0
    else:
        # 退化：直接比较今日均量与5日前
        if len(vol_short_ma) >= 5:
            volume_increasing = vol_short_ma.iloc[-1] > vol_short_ma.iloc[-5]
        else:
            volume_increasing = True  # 数据不足时假设为真

    # 4. 量能平稳性（变异系数 = 标准差/均值）
    if volume_consistency and len(volume) >= 20:
        recent_vol = volume.iloc[-20:]  # 最近20日成交量
        cv = recent_vol.std() / recent_vol.mean() if recent_vol.mean() > 0 else 1.0
        consistent = cv <= consistency_threshold
    else:
        consistent = True

    # 5. 价格-成交量一致性（可选）
    price_ok = True
    if require_price_up and price is not None:
        # 要求当日收盘价 > 昨日收盘价（反弹日应为阳线或上涨）
        if len(price) >= 2:
            price_ok = price.iloc[-1] > price.iloc[-2]

    # 最终判定
    final = trend_ok and volume_increasing and consistent and price_ok

    indicators = {
        "vol_short_ma": round(latest_vol_short, 2),
        "vol_long_ma": round(latest_vol_long, 2),
        "trend_ratio": round(trend_ratio, 2),
        "volume_increasing": volume_increasing,
        "cv": round(cv, 3) if volume_consistency else None,
        "price_up": price_ok,
        "final": final
    }

    return final, indicators


def get_rs_ratio(close, benchmark_close, normalized=False, norm_window=20):
    """
    严格时间对齐 + 可选 normalized RS
    """

    close = pd.Series(close).copy()
    benchmark_close = pd.Series(benchmark_close).copy()

    if not isinstance(close.index, pd.DatetimeIndex):
        close.index = pd.RangeIndex(len(close))

    if not isinstance(benchmark_close.index, pd.DatetimeIndex):
        benchmark_close.index = pd.RangeIndex(len(benchmark_close))

    all_index = close.index.union(benchmark_close.index)

    close = close.reindex(all_index).ffill()
    benchmark_close = benchmark_close.reindex(all_index).ffill()

    df = pd.DataFrame({
        "asset": close,
        "benchmark": benchmark_close
    }).dropna()

    df = df[df["benchmark"] != 0]

    # -----------------------------
    # base RS
    # -----------------------------
    base_rs = df["asset"] / df["benchmark"]

    # -----------------------------
    # normalized RS（增强版）
    # -----------------------------
    if normalized:
        asset_norm = df["asset"] / df["asset"].rolling(norm_window).mean()
        bench_norm = df["benchmark"] / df["benchmark"].rolling(norm_window).mean()

        rs = asset_norm / bench_norm
    else:
        rs = base_rs

    rs = rs.replace([np.inf, -np.inf], np.nan).dropna()

    return rs


# -----------------------------
# ETF 分析函数
# -----------------------------
def analyze(
        symbol,
        base_window,
        market,
        benchmark_data
):
    """分析单只ETF信号"""

    try:
        data = fetch_etf_history(symbol=symbol)

    except Exception as e:
        print(f"{symbol} download error: {e}")
        return None

    voo_data = benchmark_data

    if data.empty or voo_data.empty:
        return None

    close = data["close"]
    volume = data["volume"]
    voo_close = voo_data["close"]

    # -----------------------------
    # 动态 window
    # -----------------------------
    # window = get_dynamic_window(close, base_window)
    window = base_window
    recent_data = close.iloc[-window:]

    # -----------------------------
    # 先找近期高点
    # -----------------------------
    high_idx = recent_data.idxmax()
    recent_high = recent_data.loc[high_idx]

    # -----------------------------
    # 只在 high 后寻找 low
    # 防止未来函数
    # -----------------------------
    after_high = recent_data.loc[high_idx:]
    recent_low = after_high.min()
    price = recent_data.iloc[-1]

    # -----------------------------
    # 回撤
    # 当前价格距离近期高点
    # -----------------------------
    drawdown = (price - recent_high) / recent_high * 100

    # -----------------------------
    # 反弹
    # 当前价格距离近期低点
    # -----------------------------
    rebound = (price - recent_low) / recent_low * 100

    # -----------------------------
    # 前期回撤
    # 必须先经历足够下跌
    # -----------------------------
    pre_drawdown = (recent_low - recent_high) / recent_high * 100

    # -----------------------------
    # Recovery Ratio
    # 当前已经修复了多少跌幅
    # -----------------------------
    if recent_high != recent_low:
        recovery_ratio = (price - recent_low) / (recent_high - recent_low)
    else:
        recovery_ratio = 1

    # -----------------------------
    # 均线趋势
    # -----------------------------
    ma_short = float(
        close.rolling(MA_SHORT).mean().iloc[-1]
    )

    ma_mid = float(
        close.rolling(MA_MID).mean().iloc[-1]
    )

    ma_long = float(
        close.rolling(MA_LONG).mean().iloc[-1]
    )

    above_ma_short = price > ma_short

    strong_trend = (
        ma_short > ma_mid
    )

    healthy_long_term = (
        price > ma_long * 0.8
    )

    # -----------------------------
    # 成交量
    # -----------------------------
    volume_ok, vol_indicators = confirm_volume_trend(
        volume=volume,
        price=close,
        short_window=5,
        long_window=20,
        min_trend_strength=1.1,
        require_price_up=False,
        volume_consistency=True,
        consistency_threshold=0.4
    )

    volume_surge = volume_ok

    # -----------------------------
    # Relative Strength
    # -----------------------------
    rs_ratio = get_rs_ratio(close, voo_close)

    rs_now = float(rs_ratio.iloc[-1])

    rs_ma20 = float(
        rs_ratio.rolling(20).mean().iloc[-1]
    )

    rs_ma50 = float(
        rs_ratio.rolling(50).mean().iloc[-1]
    )

    rs_strong_short = (
        rs_now >= rs_ma20
    )

    rs_strong_mid = (
        rs_now >= rs_ma50
    )

    rs_high60 = float(
        rs_ratio.rolling(60).max().iloc[-1]
    )

    rs_breakout = (
        rs_now >= rs_high60 * RS_BREAKOUT_FACTOR
    )

    # -----------------------------
    # 市场环境
    # -----------------------------
    bull_market = market["bull_market"]

    voo_bull = market["voo_bull"]

    # -----------------------------
    # 信号判定
    # -----------------------------

    # =============================
    # 新增：周线趋势过滤器
    # =============================
    # 将日线转换为周线（取周收盘）
    # weekly_close = close.resample("W-FRI").last()
    # weekly_ma12 = weekly_close.rolling(12).mean().iloc[-1]  # 约3个月
    # weekly_ma24 = weekly_close.rolling(24).mean().iloc[-1]  # 约6个月
    # weekly_trend_up = weekly_ma12 > weekly_ma24  # 周线趋势向上

    # -----------------------------
    # 信号判定
    # -----------------------------

    # =============================
    # STRONG BUY
    # =============================
    if (
        pre_drawdown <= SIGNAL_THRESHOLDS["STRONG_BUY"]["drawdown"]
        and rebound >= SIGNAL_THRESHOLDS["STRONG_BUY"]["rebound"]
        and recovery_ratio <= 0.8
        and strong_trend
        and volume_surge
        and healthy_long_term
        and rs_breakout
        and bull_market
        # and weekly_trend_up
    ):
        state = "🚀 STRONG BUY"

    # =============================
    # BUY
    # =============================
    elif (
        pre_drawdown <= SIGNAL_THRESHOLDS["BUY"]["drawdown"]
        and rebound >= SIGNAL_THRESHOLDS["BUY"]["rebound"]
        and recovery_ratio <= 0.8
        and above_ma_short
        and strong_trend
        and rs_strong_mid
        and voo_bull
        # and weekly_trend_up
    ):
        state = "🚀 BUY"

    # =============================
    # WATCH
    # =============================
    elif (
        pre_drawdown <= SIGNAL_THRESHOLDS["WATCH"]["drawdown"]
        and rebound >= SIGNAL_THRESHOLDS["WATCH"]["rebound"]
        and recovery_ratio <= 0.8
        and above_ma_short
        and rs_strong_short
    ):
        state = "⚪ WATCH"

    else:
        state = "⚪ No-Trade"

    # -----------------------------
    # 估值数据
    # -----------------------------
    print(f"  Fetching valuation for {symbol}...")
    valuation = get_valuation(symbol)

    # -----------------------------
    # 返回结果
    # -----------------------------
    return {

        "symbol": symbol,
        "price": round(price, 2),
        "drawdown": round(drawdown, 1),
        "rebound": round(rebound, 1),
        "pre_drawdown": round(pre_drawdown, 1),
        "recovery_ratio": round(recovery_ratio, 2),
        "rs": round(rs_now, 3),
        "state": state,
        "high": round(recent_high, 2),
        "low": round(recent_low, 2),
        "window": window,

        # ---- 估值字段 ----
        "pe_current": valuation["pe_current"],
        "pe_note":    valuation["pe_note"],
    }
