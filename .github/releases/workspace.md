## 工作空间界面更新 / Workspace UI

基于 ActivityWatch 0.14 系列的界面优化版本，由 TuSiV/activitywatch 维护。

- 全新桌面侧栏、移动端抽屉导航与更清晰的统计卡片。
- 统一 Lucide 线性图标，改进明暗主题、时间线和工作报告。
- 中英文 README、新版截图与构建说明。
- 修复 Windows 构建中 CRLF 换行导致的界面覆盖校验失败。

### 下载 / Downloads

| 平台 | 文件 |
| --- | --- |
| Windows x64 | `windows-x86_64-setup.exe` 安装包，或便携 ZIP |
| Linux x64 | AppImage、DEB 或 ZIP |
| macOS Apple Silicon | `macos-arm64-unsigned.dmg` |
| macOS Intel | `macos-x86_64-unsigned.dmg` |

本次提供标准 Qt 桌面版。安装包未使用开发者证书签名；macOS 未公证，首次启动可能受到 Gatekeeper 限制。请通过系统“隐私与安全性”设置确认来源后打开。未启用 Tauri 自动更新。

This fork release includes the redesigned workspace, consistent Lucide icons, responsive navigation, light/dark themes, and bilingual documentation. Standard Qt desktop packages are provided. Installers are not developer-signed; macOS DMGs are not notarized. Tauri updater artifacts are not included.

`SHA256SUMS.txt` 提供所有下载文件的 SHA-256 校验值。GitHub 自动生成的源码归档不包含子模块；源码构建请使用 `git clone --recursive`。
