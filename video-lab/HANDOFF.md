# HANDOFF — P0 准备核验

更新时间：2026-09-19 22:58（Asia/Shanghai，UTC+08:00）。

## 当前结论与本轮范围

- 已重新读取 `shilige46/v8paper` 的 `main:video-lab/PROJECT_PLAN.md`，确认 **v1.1，2026-09-19**。
- 核验时 main 提交：`e2fe7353437a1802dbaf7fb3d985148de3e029f7`；计划文件 blob：`c4e936dc6a631df8f4aa7985e0adbd86feda169e`。
- 用户本轮明确要求：不写代码，先核验环境并说明接下来需要下载什么、本人需要做什么；最后更新 HANDOFF。
- 当前阶段：**T0 已完成文档及部分本机环境的只读核验；本地项目定位、Dola 能力/用途和 Hypit 实际渲染仍待核验。P0 未完成。**
- 本轮只新增本交接文档。未编写程序、未安装依赖、未下载软件或视频、未生成或发布。
- main 的 video-lab 在本轮写入前只有 PROJECT_PLAN.md；根目录及 video-lab 的 AGENTS.md、video-lab/HANDOFF.md 均未找到。远端目录列表与文件 404 已交叉确认。
- 尚未确认本机 v8paper 检出目录，因此本地分支、未提交改动状态未核验；不能把当前量化工作目录当成视频项目。

## 不变的 P0 链路

真实 TikTok 候选 → 下载允许保存的参考片 → 人工选片 → Hypit/Agent 真实拆解与中文分镜 → 人工确认分镜 → Dola 人工任务包 → 用户提交并下载回填 → 片段审核 → Hypit 合成 → 人工验收最终 MP4。

Hypit 是主框架；Dola 首轮采用人工文件交接，不声称存在免费 API，不擅自换到 HypiHub。首片目标 20—35 秒、竖屏 9:16；具体镜头长度依据实际 Dola 账号能力。T5 还需依据反馈复验一次局部修改。抖音发布、监控、批量系统后置。

## 本机与依赖实测

| 项目 | 实际结果 | 判断 |
| --- | --- | --- |
| Node.js / npm | 22.19.0 / 10.9.3 | 已有；Node 满足上游 main 的 >=22.15.0 要求 |
| Python / uv | 3.12.13 / 0.12.15 | 已有；本轮不需要另装 Python 或推理模型 |
| GPU | RTX 4080，16376 MiB；驱动 591.86 | 已识别；尚未进行 Hypit 渲染测试 |
| 磁盘空闲 | C 约 83.5 GB，F 约 166 GB | 核验时快照，不是下载体积估算 |
| Hypit CLI | PATH 未找到；npm 全局清单无 @hypit/hypit | 尚未定位可用程序，不等于全盘证明未安装 |
| Hypit Skill | 当前会话无 Hypit；已查用户和当前项目常用 Skill 目录未找到 | 尚未加载/安装核验 |
| ffmpeg / ffprobe | PATH 及已查 bundled runtime bin/native 未找到 | 待定位已有副本，确实缺失再下载 |
| 浏览器 | Chrome 149.0.7827.54；Edge 153.0.4234.46 | 已有，但未验证与 Hypit 渲染兼容 |
| Dola | 未登录、未提交任务 | 模型、时长、画幅、额度、费用和输出均未知 |
| TikTok | 未检查用户实际登录会话 | 候选、下载能力尚未验证 |

上游 main 的 package.json 标记 @hypit/hypit 0.2.7；这是源码元数据，不是本机安装版本或已验证发布包。上游本地渲染组件声明 HyperFrames engine/producer 0.7.101、推荐 Chrome Headless Shell 152.0.7928.2。实际准备时以选定发布包的声明为准，不混配 main 与发布包。

已执行的只读检查包括：GitHub fetch_file 与目录/提交 API；Get-Command；Node/npm/uv/Python 版本；npm list -g --depth=0；nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader；限定目录的文件搜索和磁盘空闲检查。未执行安装、构建、渲染、媒体测试或生成任务。TikTok 下载帮助网页未完整读到；官方保存入口需在实际账号界面核验。

## 下一步由 Codex 准备的下载清单（尚未执行）

1. 定位已有 v8paper 本地目录；没有时，另行准备独立检出位置。后续项目文件限制在 video-lab，原始视频、账号记录等留在局部忽略的 local/。
2. Hypit 官方 Skill 和 @hypit/hypit 程序及必要依赖：优先项目范围安装，固定实际版本；无需为使用 Hypit 另行完整克隆上游开发仓库。
3. Hypit 本地渲染实际需要的 HyperFrames 组件，以及匹配版本的 Chrome Headless Shell；先查是否存在可复用的兼容副本。缓存尽量留项目范围，不更改全局配置。
4. 确实缺失时，从 FFmpeg 官方下载页指向的 Windows 构建下载包含 ffmpeg、ffprobe 的工具包，作为 Hypit 的媒体工具。不可用独立 FFmpeg 成片替代 Hypit 验收。
5. 找到真实候选后，保存最多三条允许下载的参考 MP4，记录作者、链接、观察时间、可见指标和媒体信息。若官方保存功能只在用户手机可用，由用户保存并传回。
6. 选片和分镜通过后，只按需要准备有相应用途依据的角色参考图、字体、音效或音乐。Dola 输出由用户从实际任务下载回填。

暂不下载大型本地视频模型、WhisperX 模型全集、批量抓取系统、监控后台或付费去水印工具。是否需要语音转录工具，待选片内容确定后判断；首轮可优先选择少对白、易拆分的参考片。

## 用户需要做什么

- 提供已有 v8paper 本地目录位置（如有），便于保护原有文件和核对分支。
- 本人打开实际 Dola 官方网页/App，先不提交生成：确认是否有视频入口；记录可选时长、画幅/分辨率、输入类型、页面显示的模型名、额度/扣费提示、下载功能。未显示的字段写“未显示”；不提供密码、Cookie 或验证码。
- 确认 TikTok 可在本人正常会话中打开和播放；有现成喜欢的原链接可提供，没有则由 Codex 后续找候选。官方保存仅手机可用时，需要本人保存并传回 MP4。
- 从最多三张候选卡中选一条；随后审核中文分镜。收到 Dola 完整任务包后，按镜头逐项提交并下载，保留尝试编号及实际消耗。
- 审核生成片段和最终 MP4；问题镜头单独返工，不自动重做全部素材。
- 说明当前实际用途及可接受支出；目前新增支出授权仍为 0 元。计划中的 100 元只是建议，未获支付授权。既有工具消耗另计。

Dola 当前条款页面（2026-09-04 更新）写明私人、非商业使用范围。实际用途适用性尚未确认，不能因为还未发布或未盈利就自动认定已符合；商业使用问题未解决前不能把 P0 技术验收当作商用许可。

## 执行状态和恢复点

| 步骤 | 状态 |
| --- | --- |
| 读取 v1.1 与上游依赖文档、部分本机环境检查 | 已执行，见上述范围 |
| 本地项目检出/分支与修改核对 | 未执行完成，目录待确认 |
| 软件与素材下载、安装 | 未执行 |
| TikTok 真实候选、下载、人审选片 | 未执行 |
| Hypit 原片拆解、中文分镜、Dola 任务包 | 未执行 |
| Dola 登录能力实测、生成、下载回填 | 未执行 |
| 片段审核、Hypit 渲染、最终人工验收、局部修改复验 | 未执行 |
| 抖音发布、后台数据、监控与批量系统 | 未执行，后置 |
| 新增购买和付费生成调用 | 未执行，新增支付 0 元 |

下一最小动作：收齐本地目录、Dola 页面能力/额度信息与 TikTok 访问情况，然后在用户确认的执行范围内准备最小依赖并建立真实候选。后续首个内容交付是可追溯候选卡与可播放参考片；P0 最终交付必须包含 Hypit 可编辑项目、真实 Dola 输出、最终 MP4、审核与成本记录。

## 一手资料

- [项目 v1.1](https://github.com/shilige46/v8paper/blob/e2fe7353437a1802dbaf7fb3d985148de3e029f7/video-lab/PROJECT_PLAN.md)
- [Hypit quickstart](https://github.com/hypit-ai/hypit/blob/main/docs/zh/quickstart.md)
- [Hypit 安装与复用](https://github.com/hypit-ai/hypit/blob/main/skills/hypit/references/environment/distribution.md)
- [Hypit package.json](https://github.com/hypit-ai/hypit/blob/main/package.json)
- [本地渲染](https://github.com/hypit-ai/hypit/blob/main/packages/provider-hyperframes-local/README.md)
- [本地媒体工具](https://github.com/hypit-ai/hypit/blob/main/packages/provider-media-local/README.md)
- [Hypit LICENSE](https://github.com/hypit-ai/hypit/blob/main/LICENSE)
- [FFmpeg 下载来源](https://ffmpeg.org/download.html)
- [Dola Terms of Service](https://www.dola.com/legal/terms/en)
