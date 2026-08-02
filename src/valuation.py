# coding=utf-8
"""
估值模块
获取当前 PE（TTM），并结合 config.py 中手动录入的历史 PE 区间，
计算当前 PE 在历史区间中的百分位。

历史 PE 区间来源：Macrotrends / 富途，基于 2020-2025 年数据。
ETF、无稳定盈利标的不录入历史区间，仅展示当前 PE。
"""

import yfinance as yf
from config import PE_RANGES


def get_valuation(symbol: str) -> dict:
    """
    Returns
    -------
    dict：
        pe_current   : float | None   当前 TTM PE
        pe_5y_low    : float | None   历史 PE 低点（手动录入）
        pe_5y_high   : float | None   历史 PE 高点（手动录入）
        pe_5y_median : float | None   历史 PE 中位数（低高均值近似）
        pe_percentile: float | None   当前 PE 在历史区间的百分位（0~100）
        pe_note      : str            备注
    """
    result = {
        "pe_current":    None,
        "pe_5y_low":     None,
        "pe_5y_high":    None,
        "pe_5y_median":  None,
        "pe_percentile": None,
        "pe_note":       "",
    }

    try:
        # ── 当前 PE ──────────────────────────────────────────────────
        pe = yf.Ticker(symbol).info.get("trailingPE")
        if pe is not None:
            pe = float(pe)
            if 0 < pe < 10000:
                result["pe_current"] = round(pe, 1)

        # ── 历史区间（来自 config.py 手动录入） ──────────────────────
        pe_range = PE_RANGES.get(symbol)
        if pe_range:
            low  = pe_range.get("low")
            high = pe_range.get("high")
            if low and high and low < high:
                result["pe_5y_low"]    = low
                result["pe_5y_high"]   = high
                result["pe_5y_median"] = round((low + high) / 2, 1)
                result["pe_note"]      = pe_range.get("note", "")

                # 百分位：线性插值，当前PE在[low, high]区间的位置
                if result["pe_current"] is not None:
                    pe_cur = result["pe_current"]
                    if pe_cur <= low:
                        pct = 0.0
                    elif pe_cur >= high:
                        pct = 100.0
                    else:
                        pct = (pe_cur - low) / (high - low) * 100
                    result["pe_percentile"] = round(pct, 1)

    except Exception as e:
        result["pe_note"] = f"error: {e}"

    return result
