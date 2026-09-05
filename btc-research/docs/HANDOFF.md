# GitHub ↔ 本地 Codex 同步与交接

## 1. 固定约定

承载仓库：shilige46/v8paper。规划来源分支：docs/btc-quant-plan-20260905。项目目录：btc-research。实施分支：work/btc-m1（尚未由本次规划创建）。

规划分支和main不同；只拉main不会自动拿到未合并的规划。下载ZIP可阅读但不会保留正常Git同步流程，优先使用独立克隆。

本地大数据及原A股代码留在原位置，不能因为克隆了此仓库就上传。需要复用旧通用模块时，在用户指定的局部路径进行本地只读评估，输出脱敏的可复用性说明；未获公开授权不复制到公开仓库。

## 2. 初次读取：推荐独立新目录

以下命令在一个不属于原A股项目的父目录执行；目标目录btc-quant-work必须尚不存在，存在则停止检查，不能删除/覆盖。

```powershell
git clone --branch docs/btc-quant-plan-20260905 https://github.com/shilige46/v8paper.git btc-quant-work
cd btc-quant-work
git status --short
git switch -c work/btc-m1
cd btc-research
```

每条命令失败就停止，不继续粘贴后续写操作。以上流程不会把任何旧项目移动进来。然后在Codex中打开btc-quant-work/btc-research；已有根目录会话应显式要求读取btc-research/AGENTS.md及当前任务文档，不假设它已自动加载。

未安装Git或未登录时，先由本地环境报告实际错误；不要修改其他项目的远端、凭据或全局设置来“修复”。

## 3. 已有正确独立克隆时

先检查 `git status --short` 与 `git remote -v`，核对确为此仓库。不要在装着私有A股内容的旧工作目录直接切分支。

获取当前规划：

```powershell
git fetch origin
# 只查看远端规划，不改变当前工作树：
git show origin/docs/btc-quant-plan-20260905:btc-research/README.md
```

若本地尚无work/btc-m1且工作树干净，可以 `git switch -c work/btc-m1 origin/docs/btc-quant-plan-20260905`。已有分支则不要再次创建、不要覆盖；检查其历史与差异。

## 4. 两端不是自动聊天同步

ChatGPT端只在收到任务并实际读取GitHub时看到已推送内容；不会自行看到本地缓存、未提交文件或Codex的全部对话。Codex也不能依赖未写入仓库的聊天承诺。因此采用下列交接字段：

```text
阶段/任务：
状态：planned / in_progress / blocked / verified
代码提交：
本地工作树是否dirty：
配置哈希与数据集哈希：
真实执行命令和测试结果：
真实数据覆盖与来源：
网络验收：未运行/通过/失败及原因
回测种类：合成/历史研究/前瞻模拟/真实成交
发现的问题与限制：
本次修改文件：
Git状态：未提交/已提交未推送/已推送到指定分支
下一个最小可验收任务：
```

只上传上述脱敏摘要及允许公开的代码/测试。完整产物与数据仍在仓库外，不需要上传几百GB文件才能审查。

## 5. 更新规划与开发分支

同一实施分支约定同一时段只有一个写入方：本地Codex开发；ChatGPT优先在单独docs或review分支提交建议，不抢改未推送的代码。

在干净的work/btc-m1中，推送后再次拉取自己的远端分支可以用：

```powershell
git fetch origin
git pull --ff-only
```

仅在已设置正确upstream时执行第二条。首次获准推送为 `git push -u origin work/btc-m1`。ff-only失败说明历史已分叉，应检查差异并显式合并，不强推、不reset覆盖。

后续规划来源分支有新提交，`git pull`自己的实施分支不会自动吸收另一个分支的改动。应先fetch、比较，然后明确合并选定的规划提交或PR。未获合并授权，不自动合并main。

.gitignore仅影响未跟踪文件，不能当作绝对保密措施。每次推送之前核对 `git diff --cached --stat`、`git diff --cached`、`git status --short` 和待推送提交的文件清单；禁止直接 `git add .`。私有代码/个人路径/账户信息出现则停止推送。

## 6. 交给本地 Codex 的首轮指令

> 我要开始一个独立BTC研究项目，不修改原A股项目。请先检查当前目录、Git远端和未提交改动。在新的独立工作区读取shilige46/v8paper的docs/btc-quant-plan-20260905分支，进入btc-research，依次完整读取AGENTS.md、README.md、docs/PROJECT_SPEC.md、docs/STATUS.md、docs/superpowers/plans/2026-09-05-m1-data-baseline.md。请在work/btc-m1分支按计划执行M1，不重新设计整套系统，不接真实账户或下单。先完成隔离环境和数据保护，再按任务写失败测试、实现、验证。原A股代码/缓存不要扫描或上传。真实数据与完整结果保存在仓库外，BTC_DATA_ROOT具体路径按本机环境确定，不写入公开文档。每个任务完成更新STATUS和脱敏摘要，给出实际文件、命令、测试结果与Git状态。网络失败要如实报告，但继续完成不依赖网络的任务；不要伪造真实数据或通过结果。本轮先本地提交，推送公开仓库前列出将公开的文件并等我授权。只实施M1，完成或遇到真实阻塞时报告，不只回复一段计划。

## 7. 给 ChatGPT 的复核指令

本地已推送后发送一段即可：

> 请读取shilige46/v8paper的work/btc-m1分支，先看btc-research/docs/STATUS.md与最新docs/reviews/摘要，再审查对应实现和测试。核对数据时间、未来数据、费用、现金账本、假成交与样本外定义。请区分已经验证的问题和仅需进一步检查的假设，不要依据尚未上传的本地文件下结论。

## 官方依据

Git拉取：https://git-scm.com/docs/git-pull
Git推送：https://git-scm.com/docs/git-push
忽略规则：https://git-scm.com/docs/gitignore
Codex指令发现：https://developers.openai.com/codex/guides/agents-md

核对日期：2026-09-05。以上流程不承诺自动运行、后台处理或自动记忆。
