Atrioly · A quiet interface for modern life.  
序栖｜于纷扰人间，自置一隅静界。

# 序栖·声汐 —— 流动之声，媒介的几何  

> 声汐是 **Atrioly / 序栖** 体系下的流媒体分流与策略配置项目，  
> 专注于全球流媒体访问的智能划分、规则纯化与节点逻辑美学。  
>
> 若需**英文**版，请参考 [README.md](./README.md)  
>
> **Loon 版本**：请稳步查看 → https://github.com/Sifortonzh/Loon4Streaming  

---

# ✨ 特性亮点

- 针对主流平台的独立策略组与分流优先级（YouTube / Netflix / Disney+ / HBO Max 等）
- 按区域细分的智能节点分组：🇭🇰🇺🇸🇯🇵🇰🇷🇨🇳🇸🇬 + 🇺🇳Rare Areas自动匹配其他节点
- 常用服务：Google、GitHub、Telegram、X、TikTok、PayPal、Apple、Microsoft、AI 等
- 架构基于 Rabbit‑Spec Surge 通用骨架 + BlackMatrix7 Surge 分流规则并融入自主构建规则
- 图标来源：Koolson/Qure + Orz‑3/mini等

---

# 📦 仓库小览

```
Config4Streaming/
├─ Surge4Streaming.conf              # 主配置文件（Surge 专用）
├─ rules/                            # 各类服务域名规则列表（.list 格式）
│  ├─ AI.list
│  ├─ ESPN.list
│  ├─ Google.list
│  ├─ HBOMax.list
│  ├─ Other_US.list
│  ├─ aol.list
│  ├─ proton.list
│  └─ yandex.list
├─ modules/                          # Surge 用 JavaScript 模块脚本
├─ images/                           # 使用截图（macOS / iOS）
├─ icons/                            # 自定义图标资源
├─ README.md                         # 英文说明
└─ README-zh.md                      # 中文说明
```

---

# 🚀 快速上手（以 Surge 为例）

## 本地 MESL / SNTP 一键同步

双击 [`tools/sync.command`](./tools/sync.command)：先显示脱敏差异并校验，再选 `1` 更新 iCloud 和公开配置，或选 `2` 同时通过 SSH 发布 GitHub。首次使用先运行 `python3 tools/surge_sync.py --init`，不会改动原始配置。

- 公共模板：[`templates/Surge.shared.conf`](./templates/Surge.shared.conf)。模板内 `# @private:` 是私有字段占位符，请保留。
- 也可以继续在 iCloud 的 `MESL.conf` 或 `SNTP.conf` 修改公共规则；工具自动提取相对于上次同步的修改，并同步到另一份配置和公共模板。
- 初始化前已有的配置差异保留；新增修改发生冲突时停止，并显示脱敏冲突内容，不覆盖文件。
- 节点、订阅、证书及凭据从各自当前配置原样回填。涉及订阅的整行或 `[Proxy]` 整段作为私有内容，不跨配置同步；该行的其他选项也分别保留。
- 默认只预览；`python3 tools/surge_sync.py --apply --reload` 执行同步并重新加载当前 Surge 配置，添加 `--publish` 同步发布。使用 `--source MESL` 或 `--source SNTP` 可指定提取来源，但不会强行覆盖另一份的冲突。
- 本地基线及含隐私的备份在 Git 忽略的 `.surge-sync/`，不会提交到 GitHub。备份文件名有 `iCloud-` / `repo-` 前缀；需恢复时从对应备份复制回原文件，并同时恢复该备份的 `state.json`。不要强制提交私有目录。
- `.surge-sync/state.json` 绑定首次初始化的 iCloud 目录。其他用户通过 `--icloud /你的目录` 指定自己的位置。需要本地 Python 3、Git 和 Surge macOS 校验工具。
- 两份仓库配置作为统一公共模板的公开输出；`Surge4Streaming_0131.conf` 保留旧链接，但不再维护独立旧版逻辑。公开输出使用 `https://example.com/subscription`，使用时替换成自己的订阅。

工具会检查发布文件是否包含当前私有信息，只提交指定公共文件；已有 Git 暂存内容或远端新提交时停止发布。GitHub 推送失败时，本地同步和备份仍保留；解决 SSH/网络问题后再次运行发布即可。支持冲突检测和防覆盖检查，但不支持多人同时运行同步工具。

同步测试：`python3 -m unittest discover -s tools -p 'test_*.py'`。英文说明见 [README.md](./README.md#local-mesl--sntp-sync)。

1. 下载 [`Surge4Streaming.conf`](./Surge4Streaming.conf)。

2. 在 **Surge** → **Profiles** → **Open External Profile** 导入该文件。或从URL下载：

   ```bash
   https://raw.githubusercontent.com/Sifortonzh/Config4Streaming/refs/heads/main/Surge4Streaming.conf
   ```

3. 编辑 `policy-path=你的订阅地址` 为你的真实订阅地址。  

4. 保存并启用。

5. iOS端用“模块”需配置证书，配置方法与Loon一致。

---

# 📱效果预览

## MacOS

![Surge面板](./images/Mac.png)  

---

## iOS

![Surge面板](./images/iOS.png)

---

# 🧩 核心策略

| 组名 | 作用 | 优先顺序（左→右） |
|---|---|---|
| **YouTube** | YouTube 视频 | HK → US → SG → JP → KR → TW |
| **Netflix** | 奈飞视频 | HK  → SG → US→ Rare Areas |
| **Disney+** | 迪士尼+ | US →HK → SG → JP → KR → TW |
| **Hulu** | Hulu | US → HK →SG →  TW → JP → KR |
| **HBO Max** | HBO Max | HK →  US → SG →Rare Areas |
| **Prime Video** | 亚马逊视频 | HK → TW → JP → KR → SG → US |
| **Paramount+** | 派拉蒙+ | US → HK → SG → TW → JP → KR |
| **STARZ** | STARZ | US |
| **Google** | 谷歌服务 | HK → US → Rera Areas |
| **PayPal** | 支付 | US |
| **Rare Areas** | 其它地区自动分组 | （从“我的节点”里按负向正则筛出不含 HK/US/JP/KR/TW/SG 的节点） |

---

# 🧱 规则参考

- 核心架构：Rabbit‑Spec Surge 通用配置框架  
- 分流规则：BlackMatrix7 · Surge（YouTube / Netflix / Disney / HBO / AI / Google / Apple 等）  
- 图标设计：Koolson/Qure + Orz‑3/mini IconSet

---

# 🙌 贡献反馈

欢迎提出改进建议，或通过 issue 反馈问题。你也可以根据自身需求 fork 并维护个性化分支。
