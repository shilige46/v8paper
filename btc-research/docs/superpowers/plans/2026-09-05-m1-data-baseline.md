# M1 BTC 数据与现货基准 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. 若本地不存在这些技能，直接按本文件顺序逐项执行，不宣称调用了不存在的工具。

**Goal:** 交付一个能读取/校验公开 BTC 1m 数据、运行可逐笔复核的现货基准并输出证据的本地研究程序。

**Architecture:** 在 btc-research 内建立独立 Python 包，数据、信号、账本、模拟和报告分离。原数据与运行产物在仓库外；仓库只保留代码、测试、规划和脱敏摘要。所有真实交易功能不在 M1 范围。

**Tech Stack:** Python >=3.11；pandas、numpy、pyarrow、httpx、pytest、ruff及标准库；独立虚拟环境，实际依赖版本落入锁定文件。

**Spec:** [PROJECT_SPEC.md](../../PROJECT_SPEC.md)。本计划的文件路径均以 btc-research/ 为根，Git 命令按当前工作目录执行。

## Global Constraints

- Python 3.11 或更高版本；使用本项目虚拟环境。
- 内部统一 UTC；数据与运行产物必须在 Git 仓库根目录外。
- 1000 USDT 模拟现金；entry_fraction=0.25；fee_rate=0.001；slippage_rate=0.0005；20/10根4h突破；execution_delay_minutes=1；qty_step=0.00000001；seed=20260905。
- 所有这些值是研究假设，不是官方费率、交易过滤规则或账户事实。
- 不访问原项目私有代码/缓存，不修改根目录页面，不接真实下单。
- 先失败测试，再最小实现，再全量测试；不得通过跳过断言使任务变绿。
- 当前只完成 Task 1–7；不扩展至 Polymarket 模型或复杂前端。

## Task 1：隔离环境、配置与数据保护

**Files:** 创建 pyproject.toml、.gitignore、configs/research.example.toml、src/btc_research/__init__.py、config.py、tests/test_config.py；创建依赖锁定文件。不要修改仓库根目录的文件。

**Interfaces:** 产出 PROJECT_SPEC 定义的 ResearchConfig、load_config(path)、resolve_data_root(repo_root)。

- [ ] 确认新工作区及当前 Git 状态；记录 Python/Git 是否可用。先创建只含包发现与测试配置的 pyproject.toml，让失败来自缺失功能而不是错误的导入路径。
- [ ] 加入以下配置测试，然后运行 `python -m pytest tests/test_config.py -q`，应因接口未实现而失败：

```python
from decimal import Decimal
import pytest
from btc_research.config import load_config, resolve_data_root

def test_example_config_is_simulation_only():
    c = load_config('configs/research.example.toml')
    assert c.mode == 'historical'
    assert c.initial_cash == Decimal('1000')
    assert c.entry_fraction == Decimal('0.25')
    assert c.execution_delay_minutes == 1

def test_data_root_cannot_be_inside_repo(tmp_path, monkeypatch):
    repo = tmp_path / 'repo'
    repo.mkdir()
    monkeypatch.setenv('BTC_DATA_ROOT', str(repo / 'cache'))
    with pytest.raises(ValueError):
        resolve_data_root(repo)
```

- [ ] 最小实现：load_config 同时接受 Path 和可转换的字符串，严格校验 Spec 全部字段；resolve_data_root 用 resolve 后的路径比较。测试再覆盖未配置变量、symlink 指向仓库内部、mode='live'、负成本、entry_fraction>1、延迟为0或True。
- [ ] 写入示例 TOML：

```toml
symbol = 'BTCUSDT'
mode = 'historical'
initial_cash = '1000'
entry_fraction = '0.25'
fee_rate = '0.001'
slippage_rate = '0.0005'
entry_lookback = 20
exit_lookback = 10
execution_delay_minutes = 1
qty_step = '0.00000001'
seed = 20260905
```

- [ ] .gitignore 至少包含：`.venv/`、`__pycache__/`、`.pytest_cache/`、`.ruff_cache/`、`*.egg-info/`、`.env`、`.env.*`、`!.env.example`、`*.local.toml`、`data/`、`cache/`、`runs/`、`logs/`、`*.parquet`、`*.feather`、`*.duckdb`、`*.sqlite*`、`*.zip`、`*.csv`、`*.jsonl`、`*.log`。测试中通过内存字符串构造 CSV/ZIP，不提交真实数据。用 `git check-ignore` 检查样例路径，不创建真实密钥文件。
- [ ] 使用 `python -m venv .venv`，在新环境中安装本包与开发依赖，锁定实际版本；运行测试和 `python -m ruff check src tests`。
- [ ] 仅暂存本任务明确文件，检查 `git diff --cached --stat` 和 `git diff --cached`，提交 `chore(btc): isolate research config and storage`。不使用 git add .。

## Task 2：毫秒/微秒解析与质量闸门

**Files:** 创建 data/__init__.py、data/normalize.py、data/quality.py、tests/test_normalize.py、tests/test_quality.py。

**Interfaces:** 产出 normalize_epoch、parse_archive、audit_minutes；字段采用 Spec 数据契约。

- [ ] 先写并运行以下测试，应失败；运行 `python -m pytest tests/test_normalize.py tests/test_quality.py -q`。

```python
import pytest
from btc_research.data.normalize import normalize_epoch

def test_ms_and_us_represent_same_instant():
    a = normalize_epoch([1735689600000], 'ms')
    b = normalize_epoch([1735689600000000], 'us')
    assert a.equals(b)
    assert str(a[0]) == '2025-01-01 00:00:00+00:00'

def test_wrong_unit_is_rejected():
    with pytest.raises(ValueError):
        normalize_epoch([1735689600000000], 'ms')
```

- [ ] 用标准库 zipfile 在 tmp_path 中生成只有以下两行的合成归档，明确不是实际行情：

```text
1735689600000000,100,102,99,101,1,1735689659999999,101,2,0.5,50.5,0
1735689660000000,101,103,100,102,2,1735689719999999,204,3,1,102,0
```

- [ ] 测试 parse_archive 的列、UTC、原始十进制文本、输入SHA与 close_exclusive_utc；拒绝列数错误、空关键值、错误压缩文件、非预期多个 CSV 成员、路径穿越成员名。直接从 ZIP 读取，不向任意路径解压。
- [ ] 对上述两分钟用请求区间 2025-01-01T00:00:00Z 至 00:03:00Z 调 audit_minutes，断言 rows=2、missing_minutes=1、is_acceptable=False。再测试重复第一行、high<low、负量、请求区间外记录，各字段计数与报告明确。
- [ ] 实现对应功能；原始异常不静默丢弃或填充。保存质量报告与“不能回测”的明确异常，而不是返回一张看似正常的收益表。
- [ ] 运行本任务与 Task1 全部测试；明确暂存新增模块/测试后提交 `feat(btc): normalize spot time and audit coverage`。

## Task 3：公开归档下载与校验

**Files:** 创建 data/binance_public.py、tests/test_download.py。

**Interfaces:** 消费 Task2 解析契约；产出 fetch_day(day, root, client) 的字典收据。client 使用 httpx.Client，可注入 MockTransport；不需要任何账户认证。

- [ ] 先用 httpx.MockTransport 实现离线成功测试：返回合成 ZIP 字节，以及该 ZIP 的真实 SHA-256 文本；调用 fetch_day 后比对落盘字节、sha256、source_url 和 UTC retrieved_at。
- [ ] 下载 URL 模板为 `https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m/BTCUSDT-1m-YYYY-MM-DD.zip`，校验文件是同 URL 加 `.CHECKSUM`。仅允许日期替换；不拼接用户提供的任意路径。
- [ ] 加入校验失败测试核心断言：

```python
from datetime import date
import httpx
import pytest
from btc_research.data.binance_public import fetch_day

def test_bad_checksum_never_publishes_zip(tmp_path):
    def handler(request):
        if request.url.path.endswith('.CHECKSUM'):
            return httpx.Response(200, text='0' * 64 + '  sample.zip')
        return httpx.Response(200, content=b'not-the-expected-archive')
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ValueError):
            fetch_day(date(2025, 1, 1), tmp_path, client)
    assert not list(tmp_path.rglob('*.zip'))
```

- [ ] 运行 `python -m pytest tests/test_download.py -q` 验证失败，再实现下载：HTTPS；请求超时30秒；429/5xx最多3次尝试，退避1/2秒，服务器 Retry-After 可解析时采用其值且单次最多60秒；其他4xx直接失败。不输出凭据，不轮换身份绕过限制。
- [ ] 测试404立即失败、503两次后成功、第三次仍失败、已有同哈希文件幂等复用、已有不同内容报冲突而不覆盖、临时文件清理。Mock测试替换sleep，不实际等待。
- [ ] 下载完校验通过才原子发布 ZIP；记录来源与哈希，按归档日期显式传入 ms/us 给解析层，换算后的日期再核对。
- [ ] 离线测试和静态检查通过后提交 `feat(btc): fetch and verify public daily archives`。此步骤不宣称已验证本地联网能力。

## Task 4：完整4小时窗口与因果信号

**Files:** 创建 data/resample.py、strategy/__init__.py、strategy/breakout.py、tests/test_resample.py、tests/test_signals.py。

**Interfaces:** 消费规范化分钟表；产出 to_four_hour 表和 breakout_signals 三列信号表。

- [ ] 先构造240行连续UTC分钟、所有价格100、成交量1；断言一根4h的volume=240、边界为00:00和04:00。删除任一行，应拒绝生成完整4h并报质量错误。追加04:00这一分钟不能泄漏到前一根。
- [ ] 写下面的手算信号测试；这里只用较小窗口验证逻辑，默认策略仍为20/10：

```python
import pandas as pd
from btc_research.strategy.breakout import breakout_signals

def test_current_high_is_excluded_and_future_cannot_change_past():
    bars = pd.DataFrame({
        'close_exclusive_utc': pd.date_range('2024-12-01T04:00Z', periods=5, freq='4h'),
        'high': [100, 101, 200, 210, 500],
        'low': [98, 99, 100, 90, 80],
        'close': [99, 100, 102, 91, 490],
    })
    signals = breakout_signals(bars, entry=2, exit=2)
    assert bool(signals.iloc[2]['enter']) is True
    prefix = breakout_signals(bars.iloc[:4].copy(), entry=2, exit=2)
    pd.testing.assert_frame_equal(signals.iloc[:4], prefix)
```

- [ ] 运行 `python -m pytest tests/test_resample.py tests/test_signals.py -q` 确认失败；实现 roll(high,20).shift(1)、roll(low,10).shift(1)的等价逻辑及闭合时间约束，不把本根high/low纳入阈值。
- [ ] 增加严格大于/小于、相等不交易、warmup期间无信号、未来数据被改写但历史特征不变、窗口不连续时失败的测试。
- [ ] 全量通过后提交 `feat(btc): generate causal four-hour breakout signals`。

## Task 5：现金账本、延迟成交与样本末端

**Files:** 创建 backtest/__init__.py、backtest/accounting.py、backtest/engine.py、tests/test_accounting.py、tests/test_engine.py。

**Interfaces:** 消费 ResearchConfig、分钟表、4h表、信号；产出 buy/sell 账本变化及 run_backtest 的 trades/equity/pending_unfilled。

- [ ] 先写手算账本测试，使用零费用/零滑点对照（默认研究配置仍有成本）：

```python
from dataclasses import replace
from decimal import Decimal as D
from btc_research.config import load_config
from btc_research.backtest.accounting import buy, sell

def test_cash_and_inventory_reconcile():
    cfg = replace(load_config('configs/research.example.toml'),
                  fee_rate=D('0'), slippage_rate=D('0'))
    b = buy(D('1000'), D('0'), D('100'), cfg)
    assert b['cash'] == D('750')
    assert b['qty'] == D('2.5')
    s = sell(b['cash'], b['qty'], D('110'), cfg)
    assert s['cash'] == D('1025')
    assert s['qty'] == D('0')
```

- [ ] 写 engine 合成测试：信号在04:00形成，04:00分钟开盘100，04:01分钟开盘110；默认延迟应使用110再加滑点，不能使用100。给一个只有04:00之前数据的输入，结果应有pending_unfilled且无成交。
- [ ] 运行 `python -m pytest tests/test_accounting.py tests/test_engine.py -q` 确认失败；按Spec预算、舍入和成本公式实现。
- [ ] 每次成交验证 fee>=0、cash>=0、qty>=0、fill_time>decision_time。禁止在一个仓位上重复买入；空仓退出不产生负数量；所有成本只扣一次。
- [ ] 增加100%预算且有买入费不超支、数量舍入到0不交易、重复信号不重复建仓、末尾持仓按市值估值不隐形卖出、执行分钟缺失时报错、未来价格修改不改变此前成交的测试。
- [ ] 全量通过后提交 `feat(btc): reconcile cash and simulate delayed fills`。

## Task 6：报告、命令行与可复现清单

**Files:** 创建 reporting.py、cli.py、__main__.py、tests/test_reporting.py、tests/test_cli.py；更新README使用说明。

**Interfaces:** 消费已实现模块；产出 write_run 和以下 CLI：

```text
python -m btc_research doctor
python -m btc_research download --start 2024-12-31 --end 2025-01-02
python -m btc_research audit --start 2024-12-31 --end 2025-01-02
python -m btc_research download --start 2024-12-01 --end 2025-01-01
python -m btc_research backtest --start 2024-12-01 --end 2025-01-01 --config configs/research.example.toml
```

日期全部UTC半开区间。doctor只做环境、路径和配置检查，不发网络请求。download显式联网，其余只读本地已经验证的归档。backtest缺数据时退出非0，不自动下载、不偷用其他区间。

- [ ] 写离线报告测试：手算一笔赚25的零费案例，summary总收益=0.025，逐笔现金与权益一致；零交易不能生成无限Sharpe或假胜率。JSON的Decimal用字符串，日期为带Z的ISO8601。
- [ ] 写CLI测试：`--help`退出0；未配置BTC_DATA_ROOT的doctor退出非0并给清楚中文错误；缺数据backtest退出非0；合成小样本流程产出五个规定文件。
- [ ] 先运行测试确认缺实现导致失败，再串联各模块。run_id不覆盖已有目录。manifest按Spec包含实际code_commit与配置/数据哈希；未知值明确unknown，不能凭空生成假SHA。
- [ ] 报告加入质量覆盖、费用/滑点/延迟、样本末端未成交、估值未平仓说明、三种基准和成本/延迟假设；M1实盘可执行性明确未验证。延迟2/5分钟和成本翻倍作为敏感性输出，不据其重新选参。
- [ ] 同一输入与配置重复运行，除运行ID/时间戳外的交易、权益、指标应一致；代码/配置/数据哈希均可追踪。输出个人路径仅留本地，公开摘要用逻辑路径。
- [ ] 运行全量测试和ruff，通过后提交 `feat(btc): expose reproducible research reports and CLI`。

## Task 7：联网小样本验收与交接

**Files:** 更新 docs/STATUS.md；创建 docs/reviews/<run_id>.md（run_id由程序真实生成；路径名是动态命名规则，不是需要原样创建的尖括号文件）。

**Interfaces:** 使用 Task6 CLI 与真实本地环境。此任务不新增策略逻辑。

- [ ] 运行 `python -m pytest -q`、`python -m ruff check src tests`，保留真实输出。不能把文档里的 Expected 当成实际结果。
- [ ] 运行 doctor，然后下载/审计跨2025边界的两天，核对两种时间单位都正确。再下载2024-12整月并运行基线；若官方数据缺失或连接被拒绝，明确联网验收受阻，不改源伪造成功。
- [ ] 对报告抽查至少三种情形：一笔买入的含费现金、一筆卖出的现金、样本结尾仍持仓的权益。没有对应交易时用离线黄金样例校验，不能捏造真实交易。
- [ ] 检查假设升级：历史分钟模拟不是订单簿重放；没有实际账户费率或交易过滤规则时，输出仍只能称研究模拟。
- [ ] STATUS分别更新代码、离线测试、联网样本、模拟回测状态；报告数据覆盖、源码提交、实际命令、数据/配置哈希、限制。收益为负不删结果、不改参数“修复收益”。
- [ ] 提交前检查暂存文件名、大小和diff；不允许原始数据、zip、日志、凭据、个人绝对路径、原A股代码。单文件超过1MB必须人工检查，不凭大小判断一定安全。
- [ ] 提交 `docs(btc): record M1 verification evidence`。只有用户明确授权公开新代码和摘要后才 `git push -u origin work/btc-m1`；未推送就写“本地已提交，未推送”。不合并main。

## M1 验收清单

- [ ] 新环境安装与离线测试真实通过。
- [ ] 时间戳单位、数据完整性、闭合窗口和请求覆盖均有测试。
- [ ] 逐笔账本手算一致，费用和滑点不重算/漏算。
- [ ] 信号与历史成交通过前缀不变性测试；真实成交时间严格晚于信号。
- [ ] 缺数据不生成收益结论，未成交不补成交。
- [ ] 每次运行有来源/哈希/版本/假设/覆盖清单。
- [ ] 官方联网样本已验证，或明确仍被阻塞；阻塞不能称完整M1验收通过。
- [ ] 原A股项目、主页面、缓存和密钥未改动/未上传。
- [ ] STATUS与脱敏结果已提交；远端同步状态真实记录。

此阶段结束后先复核证据，再决定M2；不能自动开始真金白银交易。
