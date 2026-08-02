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

# =========================================================
# 历史 PE 区间（手动录入，季度粒度，数据截至 2026 年）
# 来源：Macrotrends / fullratio.com / financecharts.com
#
# 分类原则：
#   ① 商业模式稳定的成熟公司         → 10年（2016-2026）
#   ② 商业模式发生重大转变的公司      → 5年（2021-2026）
#   ③ 强周期股（能源/半导体）         → 10年（2016-2026），覆盖完整周期
#   ④ 高成长/PE区间过宽的公司         → 5年（2021-2026），或不录入
#   ⑤ 中国ADR（监管环境2021年后巨变） → 5年（2021-2026）
#
# low  = 区间内季度PE低点（剔除负PE及极端亏损季度）
# high = 区间内季度PE高点（含市场情绪溢价）
# 建议每年核查更新一次
# =========================================================
PE_RANGES = {

    # ─── ① 商业模式稳定的成熟公司（10年：2016-2026） ─────
    # KO：消费必需品，PE极稳定，低点2018年约19x，高点2020年约30x
    "KO":   {"low": 17.0, "high": 30.0, "note": "2016-2026"},  # 低点2020Q2约16x，高点2024Q3约29x
    # V：支付网络，低点2020年约25x，高点2021年约48x
    "V":    {"low": 25.0, "high": 47.0, "note": "2016-2026"},  # 低点2022Q3约25.3x，高点2021Q2约47.1x，10Y均值约33.6x
    # MCO：高护城河评级机构，低点2016年约20x，高点2021年约55x
    "MCO":  {"low": 20.0, "high": 55.0, "note": "2016-2026"},
    # AXP：信用卡，低点2016年约10x，高点2020年（EPS暴跌）约30x
    "AXP":  {"low": 10.0, "high": 33.0, "note": "2016-2026"},  # 低点2016Q2约10.6x，高点2017Q4约33x（税改）
    # BAC：银行股，低点2020年约9x，高点2021年约18x
    "BAC":  {"low": 9.0,  "high": 18.0, "note": "2016-2026"},
    # SCHW：券商，低点2020年约12x，高点2021年约38x
    "SCHW": {"low": 12.0, "high": 38.0, "note": "2016-2026"},
    # CB：保险，PE偏低稳定，低点2022年约8x，高点2020年约18x
    "CB":   {"low": 8.0,  "high": 20.0, "note": "2016-2026"},
    # KHC：食品，经历商誉减值，低点2019年约10x，高点2016年约30x
    "KHC":  {"low": 10.0, "high": 30.0, "note": "2016-2026"},
    # DVA：透析服务，PE稳定，低点2022年约10x，高点2020年约20x
    "DVA":  {"low": 10.0, "high": 22.0, "note": "2016-2026"},
    # KR：超市，低PE行业，低点2017年约12x，高点2020年约23x
    "KR":   {"low": 10.0, "high": 23.0, "note": "2016-2026"},
    # IBM：成熟转型期，低点2023年约8x，高点2017年约22x
    "IBM":  {"low": 8,  "high": 50, "note": "2020-2026"},
    # HSBC：欧洲银行，低点2020年约6x，高点2018年约15x
    "HSBC": {"low": 5.0,  "high": 20.0, "note": "2016-2026"},
    # INTC：低点2024年约8x（盈利暴跌），高点2016年约18x
    "INTC": {"low": 8.0,  "high": 30.0, "note": "2016-2026"},
    # TSM：AI需求推动2026年PE达10年新高约35x，低点2022年约12x
    "TSM":  {"low": 12.0, "high": 38.0, "note": "2016-2026"},  # 低点2022Q4约12x，2026年创历史新高约35x
    # ASML：光刻机垄断，低点2016年约20x，高点2021年约70x，2026年约55x
    "ASML": {"low": 20.0, "high": 70.0, "note": "2016-2026"},

    # ─── ② 商业模式发生重大转变（5年：2021-2026） ─────────
    # MSFT：云转型后PE中枢抬升，2026年关税冲击低点约20.7x（Jun'26季度），
    #       高点2021年约48x；2022年熊市低点约24x
    "MSFT": {"low": 20.0, "high": 40.0, "note": "2021-2026"},
    # AAPL：服务业务崛起后PE中枢抬升，2021-2026年低点2022年约21.7x，
    #       高点2024Q3约40.4x，2026年约40x仍在历史高位
    "AAPL": {"low": 21.0, "high": 41.0, "note": "2021-2026"},
    # GOOG：AI重估后EPS大幅增长压低PE，2026年约16-17x为近5年新低，
    #       高点2021年约31x；低点需纳入2026年新低
    "GOOG": {"low": 17.0, "high": 37.0, "note": "2021-2026"},  # 低点2026年7月约16.7x，高点2021年约37x
    # META：低点2022年约9x（隐私+元宇宙），5Y avg ~24，
    #       高点2021年约34x，2026年约18-21x
    "META": {"low": 9.0,  "high": 38.0, "note": "2021-2026"},
    # AVGO：并购VMware后商业模式重塑，低点2021年约25x，高点2022年约110x，
    #       2026年EPS大增后PE压缩至约56-62x
    "AVGO": {"low": 18.0, "high": 110.0,"note": "2021-2026"},

    # ─── ③ 强周期股（10年：2016-2026） ────────────────────
    # CVX：能源周期，5Y avg ~18，正常盈利8-20x，油价低谷PE虚高已剔除，
    #       2026年油价下行期PE约32x，更新高点
    "CVX":  {"low": 8.0,  "high": 35.0, "note": "2016-2026"},
    # OXY：比CVX杠杆更高，波动更大
    "OXY":  {"low": 8.0,  "high": 40.0, "note": "2016-2026"},
    # MU：半导体周期，景气低点6x，景气高点60x，2026年约17x处于周期中段
    "MU":   {"low": 6.0,  "high": 60.0, "note": "2016-2026"},
    # DAL：航空周期，正常盈利5-15x，疫情亏损期PE无效已剔除
    "DAL":  {"low": 5.0,  "high": 20.0, "note": "2016-2026"},

    # ─── ④ 高成长/区间过宽（5年：2021-2026，仅供方向参考） ─
    # NVDA：AI爆发后EPS暴增PE大幅压缩，2026年约30-34x为近年低点，
    #       高点2023年约139x；区间已纳入2026新低
    "NVDA": {"low": 25.0, "high": 140.0,"note": "2021-2026"},
    # AMZN：盈利波动剧烈，PE区间极宽，仅供方向参考
    "AMZN": {"low": 20.0, "high": 100.0,"note": "2021-2026"},
    # TSLA：成长期PE不具传统意义，低点2022年约40x，高点2021年约400x
    "TSLA": {"low": 40.0, "high": 400.0,"note": "2021-2026"},
    # AMD：从低迷到AI芯片崛起，PE区间极宽
    "AMD":  {"low": 25.0, "high": 300.0,"note": "2021-2026"},
    # ARM：2023年上市，历史数据极短，高点约320x
    "ARM":  {"low": 60.0, "high": 320.0,"note": "2023-2026"},

    # ─── ⑤ 中国ADR（2021年后监管环境巨变，用5年） ──────────
    # NTES：游戏+教育，低点2022年约12x（政策打压），高点2021年约35x
    "NTES": {"low": 12.0, "high": 35.0, "note": "2021-2026"},
    # TME：音乐流媒体，政策压制后估值回落
    "TME":  {"low": 9.0, "high": 33.0, "note": "2021-2026"},
    # FUTU：金融科技，高成长期PE极高，近年回落
    "FUTU": {"low": 10.0, "high": 120.0,"note": "2021-2026"},
    # TCEHY：腾讯，低点2022年约12x（监管+宏观），高点2021年约38x
    "TCEHY":{"low": 10.0, "high": 30.0, "note": "2021-2026"},
    # 港交所
    "HKXCY":{"low": 22.0, "high": 65.0, "note": "2021-2026"},




    # ─── 暂不录入 ──────────────────────────────────────────
    # CRWV  : 2025年上市，历史太短
    # SIRI  : 盈利不稳定
    # HKXCY : ADR，区间待核实
    # PMRTY : 新上市
    # QUBT  : 量子计算，无稳定盈利
}