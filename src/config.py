# coding=utf-8

# =========================================================
# 美股各行业ETF配置（window=120，单位：交易日）
# 每个ETF包含 window 和 category 字段
# =========================================================

ETFS = {
    # --------- 半导体/AI 芯片 ---------
    "SMH": {"window": 120, "category": "半导体核心"},       # 半导体核心ETF
    "SOXX": {"window": 120, "category": "半导体龙头"},      # 半导体龙头ETF
    "IGV": {"window": 120, "category": "软件/云计算/AI相关"},       # 软件/云计算/AI相关
    "BOTZ": {"window": 120, "category": "机器人/人工智能"},      # 机器人/人工智能ETF

    # --------- 新能源/储能/电网 ---------
    "GRID": {"window": 120, "category": "智能电网"},    # 智能电网ETF
    "LIT": {"window": 120, "category": "锂电池/储能"},     # 锂电池/储能ETF
    "BATT": {"window": 120, "category": "储能龙头"},    # 储能龙头ETF
    "TAN": {"window": 120, "category": "光伏太阳能"},     # 光伏太阳能ETF
    "FAN": {"window": 120, "category": "风电"},     # 风电ETF
    "ICLN": {"window": 120, "category": "全球清洁能源"},    # 全球清洁能源ETF
    "KARS": {"window": 120, "category": "电动车+电池"},    # 电动车+电池ETF

    # --------- 公用事业/防御ETF ---------
    "XLU": {"window": 120, "category": "公用事业/防御ETF"},    # 公用事业ETF
    "VPU": {"window": 120, "category": "公用事业/防御ETF"},    # 公用事业增强版ETF
    "IDU": {"window": 120, "category": "公用事业/防御ETF"},    # 公用事业另一版本ETF

    # --------- 数据中心/光模块/互联网 ---------
    "DJCI": {"window": 120, "category": "数据中心/光模块"},  # 数据中心/光模块ETF
    "IPAY": {"window": 120, "category": "支付/互联网"},  # 支付/互联网ETF
    "FDN": {"window": 120, "category": "电商/互联网"},   # 电商/互联网ETF
    "VGT": {"window": 120, "category": "技术成长"},   # 技术成长ETF

    # --------- 消费/电商 ---------
    "XLY": {"window": 120, "category": "可选消费"},           # 可选消费ETF
    "VOO": {"window": 120, "category": "标普500指数"},           # 标普500指数ETF
    "QQQ": {"window": 120, "category": "纳斯达克100"},           # 纳斯达克100ETF
    "VTI": {"window": 120, "category": "美股全市场"},           # 美股全市场ETF

    # --------- 金融/银行/REIT ---------
    "XLF": {"window": 120, "category": "金融/银行/REIT"},      # 金融板块ETF
    "KBE": {"window": 120, "category": "金融/银行/REIT"},      # 银行ETF
    "VNQ": {"window": 120, "category": "房地产投资信托"},      # 房地产投资信托ETF

    # --------- 健康/生物科技 ---------
    "XLV": {"window": 120, "category": "医疗健康"},       # 医疗健康ETF
    "IBB": {"window": 120, "category": "生物科技"},       # 生物科技ETF
    "XBI": {"window": 120, "category": "小盘生物科技"},       # 小盘生物科技ETF

    # --------- 能源/石油/原材料 ---------
    "XLE": {"window": 120, "category": "石油天然气"},     # 石油天然气ETF
    "USO": {"window": 120, "category": "原油"},     # 原油ETF
    "VAW": {"window": 120, "category": "原材料"},     # 原材料ETF

    # --------- 量子计算 ---------
    "QTUM": {"window": 120, "category": "量子计算/量子技术"},
    "QUBT": {"window": 120, "category": "全球量子计算行业"},
}

# =========================================
# 回撤/反弹阈值（%）
# 可根据策略调节
SIGNAL_THRESHOLDS = {
    "WATCH": {"drawdown": -15, "rebound": 7},
    "BUY": {"drawdown": -20, "rebound": 10},
    "STRONG_BUY": {"drawdown": -25, "rebound": 12}
}

# =========================================
# 均线设置
MA_SHORT = 20
MA_MID = 50
MA_LONG = 200

# =========================================
# 量化策略可调参数
VOLUME_SURGE_FACTOR = 1.3  # 成交量放大倍数
RS_BREAKOUT_FACTOR = 0.9  # RS接近新高的比例