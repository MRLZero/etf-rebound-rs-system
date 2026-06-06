# coding=utf-8
"""
估值模块 - 获取当前 PE（TTM）
数据来源：yfinance info["trailingPE"]
"""

import yfinance as yf


def get_valuation(symbol: str) -> dict:
    """
    Returns
    -------
    dict：
        pe_current : float | None   TTM PE
        pe_note    : str            备注
    """
    result = {"pe_current": None, "pe_note": ""}
    try:
        pe = yf.Ticker(symbol).info.get("trailingPE")
        if pe is not None:
            pe = float(pe)
            if 0 < pe < 10000:
                result["pe_current"] = round(pe, 1)
    except Exception as e:
        result["pe_note"] = f"error: {e}"
    return result
