# 桓亭·声汐 —— 流动之声，媒介的几何  

> 声汐是「桓亭」（Wannatring）体系下的流媒体分流与策略配置项目，  
> 专注于全球流媒体访问的智能划分、规则纯化与节点逻辑美学。  
>
> 若需**英文**版，请参考 [README.md](./README.md)  
>
> **Loon 版本**：请稳步查看 → https://github.com/Sifortonzh/Loon4Streaming  

---

## ✨ 特性亮点

- 针对主流平台的独立策略组与分流优先级（YouTube / Netflix / Disney+ / HBO Max 等）
- 按区域细分的智能节点分组：🇭🇰🇺🇸🇯🇵🇰🇷🇨🇳🇸🇬 + 🇵🇷Rare Areas 自动匹配其他节点
- 常用服务：Google、GitHub、Telegram、X、TikTok、PayPal、Apple、Microsoft、AI 等
- 架构基于 Rabbit‑Spec Surge 通用骨架 + BlackMatrix7 Surge 分流规则并融入自主构建规则
- 图标来源：Koolson/Qure + Orz‑3/mini等

---

## 📦 仓库小览

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

## 🚀 快速上手（以 Surge 为例）

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

## 🧩 核心策略

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

## 🧱 规则参考

- 核心架构：Rabbit‑Spec Surge 通用配置框架  
- 分流规则：BlackMatrix7 · Surge（YouTube / Netflix / Disney / HBO / AI / Google / Apple 等）  
- 图标设计：Koolson/Qure + Orz‑3/mini IconSet

---

## 🙌 贡献反馈

欢迎提出改进建议，或通过 issue 反馈问题。你也可以根据自身需求 fork 并维护个性化分支。

---

## 🛫 自用机场

- [**花云（Flower）**：大名鼎鼎，不用过多介绍。基本上是流媒体人的第一选择。~~因为用不起TAG,bushi~~](https://api-flowercloud.com/aff.php?aff=13383)
- [**歪兔（YToo）**：Flower的子站，功能一致，费用略低。送一个我不怎么觉得好用的Emby](https://y-too.com/aff.php?aff=7148)
- [**守候网络（SNTP）**：中高端的高性价比专线机场（赠送高质量Emby服）](https://d.xn--hwqp2zit2amna.net/auth/register?code=BcADJolY)
