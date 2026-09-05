# BTC 研究项目设计规范 v1

日期：2026-09-05。状态：M1 可供本地实施的规划；本文件不是策略有效性的证明。

## 1. 目标与边界

建立可复核的 BTC 数据与现货研究基线，再研究 Binance 信息对 Polymarket 概率定价是否有增量价值。先检验系统正确，再检验经济优势。没有承诺收益目标，不以必须赚钱作为工程验收条件。

本轮只规划；本地实施首先完成 M1。M1 不接交易账户、不调用下单接口、不涉及永续、借币、期权、充值或跨平台对冲。Polymarket 的实时采集及模型属于后续独立阶段。

本目录独立于仓库原页面和本地 A 股系统。可复用的一般思想是数据校验、日志、配置和测试方法；不能默认复用未审查代码，更不能自动上传原私有代码。

## 2. 技术与文件边界

Python 3.11 或更高版本；使用本项目虚拟环境。M1 依赖限定为 pandas、numpy、pyarrow、httpx、pytest、ruff；标准库使用 pathlib、dataclasses、decimal、tomllib、hashlib、zipfile、argparse。实施时记录实际解析的版本并生成可复现锁定文件，不把未验证的最新版本硬写成已安装版本。

计划结构：

```text
btc-research/
  AGENTS.md
  README.md
  pyproject.toml                    # M1 创建
  .gitignore                        # M1 创建，仅作用于本目录
  configs/research.example.toml      # 无凭据、无个人路径
  src/btc_research/
    __init__.py
    __main__.py
    config.py                       # 配置及仓库外输出路径
    data/binance_public.py          # 公开归档下载、校验和
    data/normalize.py               # 毫秒/微秒与规范化列
    data/quality.py                 # 缺失、重复、OHLC 校验
    data/resample.py                # 完整 1m -> 4h
    strategy/breakout.py            # 只生成入场/退出信号
    backtest/accounting.py          # 现金、数量、成本
    backtest/engine.py              # 时间顺序和成交模型
    reporting.py                    # 指标与可复核运行清单
    cli.py                          # 命令行入口
  tests/                            # 只用小型合成数据
  docs/reviews/                     # 只允许脱敏摘要
  docs/STATUS.md
```

所有运行数据由环境变量 `BTC_DATA_ROOT` 指向仓库外目录。未配置或解析后的真实路径落在仓库内，程序直接报错；检查符号链接解析后的路径。路径具体值不得写入公开摘要。

外部数据根目录分为 raw、normalized、runs 三类；命名和覆盖策略由运行 ID 管理。原归档只读保留，先写临时文件再原子替换，禁止静默覆盖不同内容。

## 3. M1 配置契约

`ResearchConfig` 为不可变 dataclass，字段及默认值：

| 字段 | 值/含义 |
|---|---|
| symbol | BTCUSDT，仅现货 |
| mode | historical；其他值报错 |
| initial_cash | Decimal('1000')，单位 USDT |
| entry_fraction | Decimal('0.25')，每次入场最多使用当时现金的 25%，含买入费 |
| fee_rate | Decimal('0.001')，单边模拟费率假设，不是官方账户费率 |
| slippage_rate | Decimal('0.0005')，单边不利滑点假设 |
| entry_lookback | 20 根完整 4h |
| exit_lookback | 10 根完整 4h |
| execution_delay_minutes | 1，收盘边界后一分钟模拟执行 |
| qty_step | Decimal('0.00000001')，模拟数量步长，不代表交易所 LOT_SIZE |
| seed | 20260905 |

费用以 USDT 记账；不计算稳定币兑美元损益。若未来研究需要转换，单独建立汇率时间序列。本配置不代表用户实际余额或仓位建议。

费率、滑点均须 >= 0 且 < 1；现金 > 0；entry_fraction 在 (0,1]；lookback 为正整数；延迟为至少 1 的整数分钟；qty_step > 0。不得接受 bool 作为整数。

数量、现金和费用使用 Decimal；信号指标允许浮点，但账本输入必须由原始十进制字符串转换，不能由 float 直接构造 Decimal。

## 4. 数据契约

M1 首先支持 Binance 公开的 BTCUSDT 现货 1m 日归档及其校验文件。公开数据按日/月提供，现货归档从 2025-01-01 起使用微秒时间戳，见官方仓库。下载记录 source_url、UTC 获取时间、SHA-256、声明单位、覆盖区间和数据版本；不能把本次下载时间当成历史交易时可获得时间。

原 CSV 为官方 12 列顺序。规范化最小字段：open_time_utc、close_exclusive_utc、open、high、low、close、volume、quote_volume、trade_count、taker_buy_base、taker_buy_quote、source_sha256。价格和成交量保留原十进制字符串供账本使用，可额外派生浮点数列供指标使用。

`open_time_utc` 是分钟开始，`close_exclusive_utc = open_time_utc + 1 minute`。保留原始 close time 用于校验，但不把官方的闭区间结束时间直接用作重采样边界。

声明单位只能为 ms 或 us。单位和数值换算后应落在 2010-01-01 至 2100-01-01 的合理范围，且与请求日/文件声明日期一致。遇到混合单位或不一致必须报错，不逐行猜测、静默修复。

质量报告字段：requested_start_utc、requested_end_utc（半开区间）、observed_start_utc、observed_end_utc、rows、missing_minutes、duplicate_minutes、invalid_ohlc_rows、negative_volume_rows、out_of_range_rows、is_acceptable、source_hashes。重复计数为重复键中超出第一条的行数；缺失由请求区间完整分钟索引计算，不仅从实际首尾推断。

有效 OHLC：low <= min(open,close) <= max(open,close) <= high；价格 > 0；volume/quote volume 非负；trade_count 为非负整数；所有关键字段非空。原始记录乱序可显式排序并记录，但冲突重复不能自动选一条。

M1 对缺失、重复、异常或请求覆盖不足采用严格失败策略：质量报告照常写出，但不生成收益结果。不能前向填充价格来伪造可交易 K 线。最后未闭合分钟不能进入数据集；可获得时间与分钟闭合时间的差异在报告中声明为历史研究假设。

4h 窗口固定 UTC 00/04/08/12/16/20 点开始，半开区间，每窗口必须恰好 240 个不同的完整分钟。open/close 取首末值，high/low 取极值，量求和。缺一根就不能输出一根“完整 4h”；M1 严格模式中止并报告。

## 5. 基准策略与成交模型

只做多和空仓，不杠杆、不加仓、不借贷。第 t 根 4h 完全闭合后，计算此前 20 根（不含 t）的最高价；close[t] 严格大于该值时产生入场候选。退出为 close[t] 严格小于此前 10 根（不含 t）的最低价。相等不触发；历史不足时不产生信号。

同一时点：持仓时只处理退出，空仓时只处理入场；不在同一信号时点先卖再买。不做每根 K 线再平衡。一次入场建立一个仓位，退出全部卖出。

信号时间为 t.close_exclusive_utc；执行时间为其后一整分钟的开始。例如 00:00–04:00 的收盘信号，在 04:01 的 1m 开盘价基础上加不利滑点模拟成交。这样不假装收盘信号可以在同一时点的历史价格无延迟成交。该模型仍是历史近似，不是证明当时盘口能成交；必须另做延迟 2/5 分钟和更高成本敏感性比较。

末端没有执行分钟时记录 pending_unfilled，不用最后收盘价补成交。执行分钟缺失时严格报错。持仓在样本结尾按最后有效 close 估值；不暗中强制平仓。如果输出额外强平对照，必须单独标识并计入退出费。

买入预算 B = cash * entry_fraction（含手续费），成交价 P = minute_open * (1 + slippage_rate)，数量 Q 向下取整到 qty_step，使 Q*P*(1+fee_rate) <= B。现金减少 Q*P + fee。卖出价 P = minute_open * (1-slippage_rate)，现金增加 Q*P-fee；卖出数量不得超过持仓。逐笔检查 cash >= 0、qty >= 0。

等式 cash + qty * mark_price = equity 必须可核对。记录手续费与滑点影响，不把本金投入当作亏损。收益指标区分已实现损益、未实现损益、现金和资产权益。

## 6. 核心接口（实施时保持一致）

所有模块位于 src/btc_research。导出的接口：

```python
# config.py
load_config(path: Path) -> ResearchConfig
resolve_data_root(repo_root: Path) -> Path
# data/binance_public.py
fetch_day(day: date, root: Path, client: httpx.Client) -> dict
# dict: path(str), sha256(str), source_url(str), retrieved_at_utc(str)
# data/normalize.py
normalize_epoch(values: list[int], unit: str) -> pd.DatetimeIndex
parse_archive(path: Path, unit: str) -> pd.DataFrame
# data/quality.py
audit_minutes(df: pd.DataFrame, start_utc: str, end_utc: str) -> dict
# data/resample.py
to_four_hour(df: pd.DataFrame) -> pd.DataFrame
# strategy/breakout.py
breakout_signals(bars: pd.DataFrame, entry: int, exit: int) -> pd.DataFrame
# returns columns: decision_time_utc, enter(bool), exit(bool)
# backtest/accounting.py
buy(cash: Decimal, qty: Decimal, price: Decimal,
    config: ResearchConfig) -> dict
sell(cash: Decimal, qty: Decimal, price: Decimal,
     config: ResearchConfig) -> dict
# returns cash, qty, fee, filled_qty, fill_price (all Decimal)
# price argument is raw minute open; functions apply slippage once
# backtest/engine.py
run_backtest(minutes: pd.DataFrame, bars: pd.DataFrame,
             signals: pd.DataFrame, config: ResearchConfig) -> dict
# returns trades(list[dict]), equity(list[dict]), pending_unfilled(list[dict])
# reporting.py
write_run(result: dict, manifest: dict, output_dir: Path) -> Path
# writes manifest.json, trades.csv, equity.csv, summary.json, report.md
```

子包各创建 __init__.py。manifest 至少包含：run_id、code_commit、dirty、config_sha256、dataset_sha256、数据覆盖与来源、Python/依赖版本、费用/滑点/延迟、信号规则版本、质量状态、随机种子、运行命令、数据种类 real/synthetic、交易所过滤规则是否验证。未验证应明确 false，不能称交易可执行。

## 7. 评价与样本隔离

M1 只做工程 smoke test。先用 2024-12-31 和 2025-01-01 两天检查单位切换，再用 2024-12 整月验证基线流水；少量历史不证明长期盈利。样本不足 warmup 也应给出正常的零交易或明确说明，不能放宽规则凑交易。

后续正式实验预留：2022–2024 设计/训练，2025 验证，2026-01-01 至 2026-09-01 UTC 半开区间为锁定测试候选。先登记配置哈希和数据覆盖，才运行锁定测试。研究者若已看过、据其调参，必须标为已消耗并另立未来前瞻区间，不能仍称未见样本。不能将 BTC 历史长度套用于 Polymarket。

比较现金基准、25% 初始买入后持有基准与100%买入持有背景对照。买入持有使用与策略相同的首个可交易时间、滑点、费用，结尾同样按市值估值。100%背景对照风险敞口不同，不直接声称超额收益。报告总收益、最大回撤、手续费、换手、持仓时间比例、交易数、逐月收益及最差区间。交易数太少、方差为0时，相关统计输出 unavailable，不编造稳定性。

长期 Sharpe 以 UTC 日收益、365 天年化、无风险收益0作为显式研究约定；M1 小样本报告不强调年化。M3 才进行分块重采样、概率校准、Brier/对数损失、交易成本稳健性等统计研究。

## 8. 学习顺序与阶段停止条件

在开发中同步完成术语说明：BTC/USDT与BTC/USD → 现货与永续差异 → maker/taker、盘口与滑点 → 现金账本 → 二元合约概率与净期望 → 数据时钟和结算规则。每阶段报告用中文解释本阶段新增的概念，避免只有术语或一张收益图。

M1 任一关键不变量或数据完整性失败，应停止收益结论并修复。M3 若样本外不优于简单基准、概率不校准、成本/延迟压力使优势消失，则记录否定结果，不循环调参直到通过。下一阶段是否开始与实盘是否授权，均分别决定。

## 9. 核对过的官方资料

- Binance 公开归档、字段、单位与校验和：https://github.com/binance/binance-public-data
- Polymarket 显示价格与真实买卖盘：https://docs.polymarket.com/concepts/prices-orderbook
- 价格历史接口：https://docs.polymarket.com/api-reference/markets/get-prices-history
- 实时数据与价格参考源：https://docs.polymarket.com/market-data/realtime-data
- 动态费率与市场配置：https://docs.polymarket.com/trading/fees

核对日期为 2026-09-05。接口、费率和市场规则会变化；实施时重新读取对应官方说明并存取用版本，不复用社交媒体截图中的常量。
