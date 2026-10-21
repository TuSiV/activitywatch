<h1 align="center">ActivityWatch</h1>
<p align="center"><strong>Workspace Edition</strong></p>
<p align="center">看清时间去向，轻松回顾一天。</p>

<p align="center">
  <a href="README.md"><strong>简体中文</strong></a> · <a href="README.en.md">English</a>
</p>
<p align="center">
  <a href="https://github.com/TuSiV/activitywatch/actions/workflows/workspace-ui.yml"><img src="https://github.com/TuSiV/activitywatch/actions/workflows/workspace-ui.yml/badge.svg?branch=main" alt="Workspace UI 构建与测试"></a>
  <a href="LICENSE.txt"><img src="https://img.shields.io/badge/license-MPL--2.0-64748b?style=flat" alt="MPL-2.0 许可"></a>
  <a href="https://github.com/ActivityWatch/activitywatch"><img src="https://img.shields.io/badge/based_on-ActivityWatch-64748b?style=flat" alt="基于 ActivityWatch"></a>
</p>
<p align="center">
  <a href="#功能一览">功能一览</a> · <a href="#开始使用">开始使用</a> · <a href="ui-overrides/README.md">开发与维护</a> · <a href="https://docs.activitywatch.net/">上游文档</a>
</p>

基于 [ActivityWatch](https://github.com/ActivityWatch/activitywatch) 的社区维护分支。保留自动时间记录与本地数据能力，重新整理导航、图表和工作报告，让日常查看与复盘更直接。

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/images/workspace-dark.png">
  <img src=".github/images/workspace-light.png" alt="新版活动总览：侧栏导航、活跃时长、应用排行与时间分布" width="1440">
</picture>
<p align="center"><sub>当前代码的实际渲染截图，使用合成演示数据。截图随 GitHub 深浅主题切换。</sub></p>

## 功能一览

| 你想了解什么 | 对应入口 | 可以做什么 |
| --- | --- | --- |
| 今天的时间花在哪里 | 活动 | 按日期和设备查看活跃时长、应用、窗口标题与分类分布 |
| 某一时段发生了什么 | 时间线 | 浏览事件，按设备、客户端、时长和分类筛选 |
| 如何按自己的方式归类 | 分类构建器 | 管理分类规则、分类树与颜色 |
| 一段时间工作了多久 | 工作报告 | 选择设备、分类与日期，查看时段统计，导出 CSV / JSON |
| 如何主动记录一段任务 | 秒表 | 开始、停止并标记计时记录 |
| 如何检查或迁移记录 | 原始数据 | 查看数据桶与事件，导入、导出活动数据 |

浏览器标签页、标题和 URL 的采集需要对应的浏览器扩展；更多采集能力来自独立 watcher。参见[采集器文档](https://docs.activitywatch.net/en/latest/watchers.html)。

## 更清楚的工作界面

- **导航更集中**：桌面使用固定侧栏，窄屏使用抽屉菜单。
- **图表更有层次**：活跃时长突出显示，排行独立成卡，时间分布使用宽栏。
- **深浅主题一致**：统一文字、边框、背景和图表刻度，保留用户分类颜色。
- **图标更轻**：统一圆角线性图标、尺寸与对齐，保留品牌图标及扩展兼容。
- **报告更直观**：先看工作总时长、时段数量与平均时长，再看每日明细。

<details>
<summary><strong>查看窄屏界面</strong></summary>
<br>
<p align="center"><img src=".github/images/workspace-mobile.png" alt="手机尺寸下的活动界面，使用深色主题与演示数据" width="320"></p>

</details>

## 开始使用

**定制界面当前通过源码构建获取，本仓库尚未发布公开安装包。** 后续安装包以[本仓库 Releases](https://github.com/TuSiV/activitywatch/releases) 的附件与说明为准。

### 构建完整桌面套件

先按[上游源码构建指南](https://docs.activitywatch.net/en/latest/installing-from-source.html)准备 Python、Poetry、Node.js、Make、Rust 及对应平台依赖，并激活 Python 虚拟环境。本仓库前端 CI 使用 Node.js 22。

```sh
git clone --recurse-submodules --branch main https://github.com/TuSiV/activitywatch.git
cd activitywatch
make build
aw-qt
```

启动后访问 [localhost:5600](http://localhost:5600/)。`aw-qt` 负责管理本地服务与默认采集器；首次使用可参照[入门指南](https://docs.activitywatch.net/en/latest/getting-started.html)。

<details>
<summary><strong>只构建或开发前端</strong></summary>

在已克隆并初始化子模块的仓库根目录执行：

```sh
python scripts/apply_webui_theme.py --webui aw-server/aw-webui
make -C aw-server/aw-webui build
```

静态产物位于 `aw-server/aw-webui/dist/`。开发服务器使用 `make -C aw-server/aw-webui dev`；默认连接 `127.0.0.1:5666`，需要同时运行测试模式后端。

</details>

### 第一次使用

1. 确认本地服务、窗口采集器和离开状态采集器已运行。
2. 在“活动”中选择设备、日期或时间范围。
3. 在“分类构建器”中调整自己的规则，在“设置”中选择语言与主题。
4. 需要汇总时，进入“工作报告”计算并导出。

## 数据与隐私

活动记录由本地 ActivityWatch 服务保存。记录内容可包含应用名称、窗口标题，以及浏览器扩展采集的标题和 URL；启用的采集器决定数据范围。请在分享导出文件或截图前检查其内容。

新版图标随代码本地打包，不依赖远程图标服务。更新检查、浏览器扩展等联网行为由对应功能和设置决定。

## 开发与维护

本仓库通过 Git 子模块组合上游组件，定制界面保存在 `ui-overrides/`。根目录的 `make build` 会应用带校验的覆盖文件；更新上游后若文件发生变化，构建会给出需要复核的路径。

| 位置 | 用途 |
| --- | --- |
| [`ui-overrides/`](ui-overrides/README.md) | 界面源码、图标、样式及覆盖维护说明 |
| [`scripts/apply_webui_theme.py`](scripts/apply_webui_theme.py) | 验证并应用定制前端 |
| [Workspace UI 检查](https://github.com/TuSiV/activitywatch/actions/workflows/workspace-ui.yml) | 回归测试、语言校验与生产构建 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 上游贡献流程与开发约定 |

代码改进可通过[本仓库 Pull Requests](https://github.com/TuSiV/activitywatch/pulls)提交。通用使用问题可在 [ActivityWatch Forum](https://forum.activitywatch.net/) 讨论。

## 致谢与许可

- 原项目：[ActivityWatch](https://github.com/ActivityWatch/activitywatch)，由 Erik Bjäreholt、Johan Bjäreholt 及社区贡献者开发。
- 本分支维护与界面定制：[YONGZHE CHEN · TuSiV](https://github.com/TuSiV)。
- 项目许可：[MPL-2.0](LICENSE.txt)；线性图标来自 Lucide，许可见 [ISC notice](ui-overrides/static/licenses/lucide.txt)。各子模块保留其原有署名与许可。
- 学术引用沿用[上游引用信息](https://github.com/ActivityWatch/activitywatch#how-to-cite-activitywatch)与 [`CITATION.cff`](CITATION.cff)。
