# coding=utf-8
"""
估值模块
获取当前 PE（TTM）以及近5年 PE 历史区间

数据来源优先级：
  1. 当前PE  → yfinance info["trailingPE"]（实时，最可靠）
  2. 历史区间 → FMP API（/historical-price-full/ratios，季度级别，与专业平台一致）
  3. 历史区间 → Macrotrends 网页抓取（FMP 失败时 fallback）
  4. 历史区间 → yfinance Diluted EPS 自建（最后兜底）

FMP API：
  - 需要环境变量 FMP_API_KEY
  - 免费账户 250次/天，60个标的每次运行约消耗 60次，足够日常使用
  - 接口：https://financialmodelingprep.com/api/v3/historical-price-full/ratios/{symbol}
"""

import os
import re
import time
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

# ─────────────────────────────────────────
# FMP 配置
# ─────────────────────────────────────────
_FMP_API_KEY = os.getenv("FMP_API_KEY", "")
_FMP_BASE = "https://financialmodelingprep.com/api/v3"

# ─────────────────────────────────────────
# Macrotrends 配置
# ─────────────────────────────────────────
_MT_BASE = "https://www.macrotrends.net/stocks/charts"

_MT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.macrotrends.net/",
}

_MT_REQUEST_DELAY = 1.5  # 秒，避免被限速

# Macrotrends slug 手动映射（自动转换失败的特殊标的）
_MT_SLUG_OVERRIDES = {
    "BRK.B": ("BRK-B", "berkshire-hathaway"),
    "BRK.A": ("BRK-A", "berkshire-hathaway"),
    "TSM": ("TSM", "taiwan-semiconductor"),
    "TCEHY": ("TCEHY", "tencent"),
    "NTES": ("NTES", "netease"),
    "ASML": ("ASML", "asml-holding"),
    "HKXCY": ("HKXCY", "hong-kong-exchanges"),
    "TME": ("TME", "tencent-music"),
    "PMRTY": ("PMRTY", "pop-mart-international"),
    "HSBC": ("HSBC", "hsbc-holdings"),
}


# ═════════════════════════════════════════
# 第2层：FMP API
# ═════════════════════════════════════════
def _fetch_fmp_pe(symbol: str) -> pd.Series | None:
    """
    通过 FMP /historical-price-full/ratios 接口获取季度 PE 历史数据。

    FMP 直接返回每个季度末的 priceEarningsRatio，
    数据来源与 Bloomberg/富途等专业平台一致。

    返回 pd.Series（index=date, values=pe_ratio），或 None（失败）。
    """
    if not _FMP_API_KEY:
        return None

    url = f"{_FMP_BASE}/historical-price-full/ratios/{symbol}"
    params = {
        "period": "quarter",
        "apikey": _FMP_API_KEY,
        "limit": 40,  # 10年 × 4季度，足够覆盖5年区间
    }

    try:
        resp = requests.get(url, params=params, timeout=10)

        if resp.status_code == 401:
            print(f"  [valuation] FMP API key invalid or expired")
            return None
        if resp.status_code == 429:
            print(f"  [valuation] FMP rate limit reached")
            return None
        if resp.status_code != 200:
            print(f"  [valuation] FMP HTTP {resp.status_code} for {symbol}")
            return None

        data = resp.json()

        # FMP 响应结构：{"symbol": "MCO", "historicalRatios": [...]}
        # 每条记录含：date, priceEarningsRatio, ...
        historical = data.get("historicalRatios") or data.get("historical") or []

        if not historical:
            return None

        records = []
        for item in historical:
            date_str = item.get("date", "")
            pe = item.get("priceEarningsRatio") or item.get("peRatio")
            if not date_str or pe is None:
                continue
            try:
                pe = float(pe)
                if pe > 0:  # 过滤负PE和零值
                    records.append({
                        "date": pd.to_datetime(date_str),
                        "pe_ratio": pe,
                    })
            except (ValueError, TypeError):
                continue

        if not records:
            return None

        series = (
            pd.DataFrame(records)
            .set_index("date")["pe_ratio"]
            .sort_index()
        )

        return series

    except Exception as e:
        print(f"  [valuation] FMP error ({symbol}): {e}")
        return None


# ═════════════════════════════════════════
# 第3层：Macrotrends 网页抓取
# ═════════════════════════════════════════
def _name_to_mt_slug(name: str) -> str:
    """公司名 → Macrotrends URL slug。"""
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def _get_mt_slug(symbol: str, info: dict) -> tuple[str, str]:
    """返回 (ticker_for_url, name_slug)。"""
    if symbol in _MT_SLUG_OVERRIDES:
        return _MT_SLUG_OVERRIDES[symbol]
    long_name = info.get("longName") or info.get("shortName") or symbol
    return symbol, _name_to_mt_slug(long_name)


def _fetch_macrotrends_pe(symbol: str, ticker_url: str, slug: str) -> pd.Series | None:
    """
    抓取 Macrotrends PE ratio 页面，解析季度历史表格。
    返回 pd.Series（index=date, values=pe_ratio），或 None。
    """
    url = f"{_MT_BASE}/{ticker_url}/{slug}/pe-ratio"
    try:
        time.sleep(_MT_REQUEST_DELAY)
        resp = requests.get(url, headers=_MT_HEADERS, timeout=15)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "lxml")

        target = None
        for t in soup.find_all("table"):
            header = t.find("tr")
            if header and "PE Ratio" in header.get_text():
                target = t
                break

        if target is None:
            return None

        records = []
        for row in target.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            try:
                date = pd.to_datetime(cols[0].get_text(strip=True))
                pe = float(cols[3].get_text(strip=True))
                if pe > 0:
                    records.append({"date": date, "pe_ratio": pe})
            except (ValueError, TypeError):
                continue

        if not records:
            return None

        return (
            pd.DataFrame(records)
            .set_index("date")["pe_ratio"]
            .sort_index()
        )

    except Exception as e:
        print(f"  [valuation] Macrotrends error ({symbol}): {e}")
        return None


# ═════════════════════════════════════════
# 第4层：yfinance 自建（最后兜底）
# ═════════════════════════════════════════
def _build_pe_series_yf(ticker: yf.Ticker, pe_current: float | None = None) -> pd.Series | None:
    """
    用 yfinance 季度 Diluted EPS + 不复权历史价格构造 PE 序列。
    直接用财报稀释EPS（含当期加权股本），避免用当前股本除历史净利润的误差。
    含 ADR 外币单位一致性校验。
    """
    try:
        q_fin = ticker.quarterly_income_stmt
        if q_fin is None or q_fin.empty:
            return None

        if "Diluted EPS" in q_fin.index:
            eps_q = q_fin.loc["Diluted EPS"].sort_index()
        elif "Basic EPS" in q_fin.index:
            eps_q = q_fin.loc["Basic EPS"].sort_index()
        else:
            return None

        eps_q = pd.to_numeric(eps_q, errors="coerce").dropna()
        if eps_q.empty:
            return None

        ttm_eps = eps_q.rolling(4, min_periods=4).sum().dropna()
        if ttm_eps.empty:
            return None

        hist = ticker.history(period="5y", interval="1d", auto_adjust=False)
        if hist.empty:
            return None

        price_daily = hist["Close"].copy()
        price_daily.index = pd.to_datetime(price_daily.index).tz_localize(None)
        ttm_eps.index = pd.to_datetime(ttm_eps.index).tz_localize(None)

        eps_daily = (
            ttm_eps
            .reindex(price_daily.index.union(ttm_eps.index))
            .sort_index()
            .ffill()
            .reindex(price_daily.index)
        )

        pe_series = (price_daily / eps_daily).replace([np.inf, -np.inf], np.nan).dropna()
        pe_series = pe_series[(pe_series > 0) & (pe_series < 500)]

        if pe_series.empty:
            return None

        # ADR 外币单位校验：中位数与当前PE相差5倍以上则丢弃
        if pe_current and pe_current > 0:
            median = float(pe_series.median())
            ratio = max(pe_current, median) / max(min(pe_current, median), 0.01)
            if ratio > 5:
                return None

        return pe_series

    except Exception:
        return None


# ═════════════════════════════════════════
# 统一计算 5Y 统计指标
# ═════════════════════════════════════════
def _calc_5y_stats(pe_series: pd.Series, pe_current: float | None) -> dict:
    """从 PE 序列截取近5年，计算 low/high/median/mean/percentile。"""
    cutoff = pd.Timestamp.now() - pd.DateOffset(years=5)
    pe_5y = pe_series[pe_series.index >= cutoff]

    if len(pe_5y) < 4:
        return {}

    stats = {
        "pe_5y_low": round(float(pe_5y.min()), 1),
        "pe_5y_high": round(float(pe_5y.max()), 1),
        "pe_5y_median": round(float(pe_5y.median()), 1),
        "pe_5y_mean": round(float(pe_5y.mean()), 1),
    }

    if pe_current and pe_current > 0:
        pct = float(np.mean(pe_5y <= pe_current)) * 100
        stats["pe_percentile"] = round(pct, 1)

    return stats


# ═════════════════════════════════════════
# 公开接口
# ═════════════════════════════════════════
def get_valuation(symbol: str) -> dict:
    """
    获取指定标的的估值信息。

    Returns
    -------
    dict：
        pe_current   : float | None   当前 TTM PE
        pe_5y_low    : float | None   近5年 PE 历史低点
        pe_5y_high   : float | None   近5年 PE 历史高点
        pe_5y_median : float | None   近5年 PE 中位数
        pe_5y_mean   : float | None   近5年 PE 均值
        pe_percentile: float | None   当前PE在近5年的百分位（0~100，越高越贵）
        pe_source    : str            数据来源（fmp / macrotrends / yfinance / N/A）
        pe_note      : str            附加备注
    """
    result = {
        "pe_current": None,
        "pe_5y_low": None,
        "pe_5y_high": None,
        "pe_5y_median": None,
        "pe_5y_mean": None,
        "pe_percentile": None,
        "pe_source": "N/A",
        "pe_note": "",
    }

    try:
        yf_ticker = yf.Ticker(symbol)
        info = yf_ticker.info

        # ── 1. 当前PE：yfinance info（实时，货币单位正确） ──────────────
        pe_current = info.get("trailingPE")
        if pe_current is not None:
            try:
                pe_current = float(pe_current)
                if pe_current <= 0 or pe_current > 10000:
                    pe_current = None
            except Exception:
                pe_current = None
        result["pe_current"] = round(pe_current, 1) if pe_current else None

        # ── 2. 历史区间：FMP API（优先） ────────────────────────────────
        fmp_series = _fetch_fmp_pe(symbol)
        if fmp_series is not None and len(fmp_series) >= 4:
            stats = _calc_5y_stats(fmp_series, pe_current)
            if stats:
                result.update(stats)
                result["pe_source"] = "fmp"
                return result
            # FMP 有数据但近5年条数不足（新股等），仍继续尝试下一层
            print(f"  [valuation] FMP data insufficient for {symbol}, trying Macrotrends")

        # ── 3. 历史区间：Macrotrends（fallback） ────────────────────────
        ticker_url, slug = _get_mt_slug(symbol, info)
        mt_series = _fetch_macrotrends_pe(symbol, ticker_url, slug)
        if mt_series is not None and len(mt_series) >= 4:
            stats = _calc_5y_stats(mt_series, pe_current)
            if stats:
                result.update(stats)
                result["pe_source"] = "macrotrends"
                return result
            print(f"  [valuation] Macrotrends data insufficient for {symbol}, trying yfinance")

        # ── 4. 历史区间：yfinance 自建（最后兜底） ──────────────────────
        print(f"  [valuation] Using yfinance fallback for {symbol}")
        yf_series = _build_pe_series_yf(yf_ticker, pe_current=pe_current)
        if yf_series is not None:
            stats = _calc_5y_stats(yf_series, pe_current)
            if stats:
                result.update(stats)
                result["pe_source"] = "yfinance"
                return result

        # 全部失败：只有当前PE
        result["pe_source"] = "N/A"
        result["pe_note"] = "current only" if pe_current else "N/A"

    except Exception as e:
        result["pe_note"] = f"error: {e}"

    return result
