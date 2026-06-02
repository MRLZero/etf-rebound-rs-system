# coding=utf-8

# =========================================================
# 美股各行业ETF配置（window=180，单位：交易日）
# 每个ETF包含 window 和 category 字段
# =========================================================

ETFS = {
    # --------- 半导体/AI 芯片 ---------
    "SMH": {"window": 180, "category": "半导体核心"},  # 半导体核心ETF
    "SOXX": {"window": 180, "category": "半导体龙头"},  # 半导体龙头ETF
    "IGV": {"window": 180, "category": "软件/云计算/AI相关"},  # 软件/云计算/AI相关
    "BOTZ": {"window": 180, "category": "机器人/人工智能"},  # 机器人/人工智能ETF

    # --------- 新能源/储能/电网 ---------
    "GRID": {"window": 180, "category": "智能电网"},  # 智能电网ETF
    "LIT": {"window": 180, "category": "锂电池/储能"},  # 锂电池/储能ETF
    "BATT": {"window": 180, "category": "储能龙头"},  # 储能龙头ETF
    "TAN": {"window": 180, "category": "光伏太阳能"},  # 光伏太阳能ETF
    "FAN": {"window": 180, "category": "风电"},  # 风电ETF
    "ICLN": {"window": 180, "category": "全球清洁能源"},  # 全球清洁能源ETF
    "KARS": {"window": 180, "category": "电动车+电池"},  # 电动车+电池ETF

    # --------- 公用事业/防御ETF ---------
    "XLU": {"window": 180, "category": "公用事业/防御ETF"},  # 公用事业ETF
    "VPU": {"window": 180, "category": "公用事业/防御ETF"},  # 公用事业增强版ETF
    "IDU": {"window": 180, "category": "公用事业/防御ETF"},  # 公用事业另一版本ETF

    # --------- 数据中心/光模块/互联网 ---------
    "DJCI": {"window": 180, "category": "数据中心/光模块"},  # 数据中心/光模块ETF
    "IPAY": {"window": 180, "category": "支付/互联网"},  # 支付/互联网ETF
    "FDN": {"window": 180, "category": "电商/互联网"},  # 电商/互联网ETF
    "VGT": {"window": 180, "category": "技术成长"},  # 技术成长ETF

    # --------- 消费/电商 ---------
    "XLY": {"window": 180, "category": "可选消费"},  # 可选消费ETF
    "VOO": {"window": 180, "category": "标普500指数"},  # 标普500指数ETF
    "QQQ": {"window": 180, "category": "纳斯达克100"},  # 纳斯达克100ETF
    "VTI": {"window": 180, "category": "美股全市场"},  # 美股全市场ETF

    # --------- 金融/银行/REIT ---------
    "XLF": {"window": 180, "category": "金融/银行/REIT"},  # 金融板块ETF
    "KBE": {"window": 180, "category": "金融/银行/REIT"},  # 银行ETF
    "VNQ": {"window": 180, "category": "房地产投资信托"},  # 房地产投资信托ETF

    # --------- 健康/生物科技 ---------
    "XLV": {"window": 180, "category": "医疗健康"},  # 医疗健康ETF
    "IBB": {"window": 180, "category": "生物科技"},  # 生物科技ETF
    "XBI": {"window": 180, "category": "小盘生物科技"},  # 小盘生物科技ETF

    # --------- 能源/石油/原材料 ---------
    "XLE": {"window": 180, "category": "石油天然气"},  # 石油天然气ETF
    "USO": {"window": 180, "category": "原油"},  # 原油ETF
    "VAW": {"window": 180, "category": "原材料"},  # 原材料ETF

    # --------- 量子计算 ---------
    "QTUM": {"window": 180, "category": "量子计算/量子技术"},
    "QUBT": {"window": 180, "category": "全球量子计算行业"},

    # --------- 7巨头 -------------
    "AAPL": {"window": 180, "category": "苹果"},
    "AMZN": {"window": 180, "category": "亚马逊"},
    "GOOG": {"window": 180, "category": "谷歌"},
    "META": {"window": 180, "category": "Meta Platforms"},
    "MSFT": {"window": 180, "category": "微软"},
    "NVDA": {"window": 180, "category": "英伟达"},
    "TSLA": {"window": 180, "category": "特斯拉"},

    # ----- 科技 -------
    "IBM": {"window": 180, "category": "IBM Corp"},
    "AVGO": {"window": 180, "category": "博通"},
    "TSM": {"window": 180, "category": "台积电"},
    "MU": {"window": 180, "category": "美光科技"},
    "AMD": {"window": 180, "category": "美国超微公司"},
    "ARM": {"window": 180, "category": "Arm Holdings"},
    "INTC": {"window": 180, "category": "英特尔"},
    "CRWV": {"window": 180, "category": "CoreWeave"},
    "ASML": {"window": 180, "category": "阿斯麦"},

    # ---- 金融 ----
    "SCHW": {"window": 180, "category": "嘉信理财"},
    "HSBC": {"window": 180, "category": "汇丰控股"},

    # ---- 巴菲特持仓 -----
    "AXP": {"window": 180, "category": "美国运通"},
    "KO": {"window": 180, "category": "可口可乐"},
    "BAC": {"window": 180, "category": "美国银行"},
    "CVX": {"window": 180, "category": "雪佛龙"},
    "OXY": {"window": 180, "category": "西方石油"},
    "MCO": {"window": 180, "category": "穆迪"},
    "CB": {"window": 180, "category": "安达保险"},
    "KHC": {"window": 180, "category": "卡夫亨氏"},
    "DVA": {"window": 180, "category": "德维特"},
    "KR": {"window": 180, "category": "克罗格"},
    "V": {"window": 180, "category": "Visa"},
    "SIRI": {"window": 180, "category": "Sirius XM"},
    "DAL": {"window": 180, "category": "达美航空"},

    # ---- 中国股 ----
    "NTES": {"window": 180, "category": "网易"},
    "TME": {"window": 180, "category": "腾讯音乐"},
    "FUTU": {"window": 180, "category": "富途"},
    "HKXCY": {"window": 180, "category": "香港交易所（ADR）"},
    "TCEHY": {"window": 180, "category": "腾讯控股（ADR）"},
    "PMRTY": {"window": 180, "category": "POP MART"},

}

# =========================================
# 回撤/反弹阈值（%）
# 可根据策略调节
SIGNAL_THRESHOLDS = {
    "WATCH": {"drawdown": -15, "rebound": 5},
    "BUY": {"drawdown": -20, "rebound": 8},
    "STRONG_BUY": {"drawdown": -25, "rebound": 9}
}

# =========================================
# 均线设置
MA_SHORT = 20
MA_MID = 50
MA_LONG = 200

# =========================================
# 量化策略可调参数
VOLUME_SURGE_FACTOR = 1.3  # 成交量放大倍数
RS_BREAKOUT_FACTOR = 0.8  # RS接近新高的比例

# 基准ETF
BENCHMARK = "VOO"
