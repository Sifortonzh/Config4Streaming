# Config4Streaming · Enjoy All Streaming

[中文 → README-zh.md](./README-zh.md)

> A Surge streaming split configuration that tries to faithfully reproduce my **Loon** setup.

- **Config file**: [`Surge4Streaming.conf`](./Surge4Streaming.conf)  
- **Loon edition**: please refer to → https://github.com/Sifortonzh/Loon4Streaming  
- **Status**: iOS/macOS screenshots included.

---

## ✨ Key Features

- **Independent policy groups and priorities** for mainstream streaming platforms (YouTube / Netflix / Disney+ / Hulu / HBO Max / Prime Video / Paramount+ / STARZ).
- Regional groups (HK/US/JP/KR/TW/SG) + smart **Rare Areas** (automatically collects other unrecognized regions).
- Common service groups (Google, GitHub, Telegram, X, TikTok, PayPal, Apple, Microsoft, AI, etc.).
- Built on **Rabbit‑Spec [ShenXiangYouMiao]** general Surge skeleton + **BlackMatrix7** rule sets for Surge.
- Icons from **Koolson/Qure** and **Orz‑3/mini**.
- Default details: Google prefers HK, PayPal via US, STARZ: US.

> **Tip**: Replace `policy-path=YOUR_SUBSCRIPTION_URL` in the config with your own Surge subscription link (or the one provided by your provider).

---

## 📦 Directory Structure

```bash
.
├─ Surge4Streaming.conf
└─ images/
   ├─ Mac-1.png
   ├─ Mac-2.png
   ├─ iOS-1.png
   ├─ iOS-2.png
   └─ iOS-3.png
```

---

## 🧭 Quick Start (Surge · macOS)

1. Download [`Surge4Streaming.conf`](./Surge4Streaming.conf).  
2. In **Surge** → **Profiles** → **Open External Profile**, import the file. Or download from URL:

   ```bash
   https://raw.githubusercontent.com/Sifortonzh/Config4Streaming/refs/heads/main/Surge4Streaming.conf
   ```
3. Edit `policy-path=YOUR_SUBSCRIPTION_URL` to your real subscription URL.  
4. Save and enable.
5. On iOS, using “Modules” requires setting up the certificate; the method is the same as in Loon.

**Screenshots (macOS)**  
![Surge Panel](./images/Mac-1.png)  
![Policy Groups Overview](./images/Mac-2.png)

---

## 📱 iOS

![Surge Panel](./images/iOS-1.png)
![Surge Panel](./images/iOS-2.png)
![Surge Panel](./images/iOS-3.png)

---

## 🧩 Policy Groups (Core)

| Group | Purpose | Priority (Left → Right) |
|---|---|---|
| **YouTube** | YouTube video | HK → US → SG → JP → KR → TW |
| **Netflix** | Netflix video | HK  → SG → US→ Rare Areas |
| **Disney+** | Disney+ | US →HK → SG → JP → KR → TW |
| **Hulu** | Hulu | US → HK →SG →  TW → JP → KR |
| **HBO Max** | HBO Max | HK →  US → SG →Rare Areas |
| **Prime Video** | Amazon Prime Video | HK → TW → JP → KR → SG → US |
| **Paramount+** | Paramount+ | US → HK → SG → TW → JP → KR |
| **STARZ** | STARZ | US |
| **Google** | Google services | HK → US → Rare Areas |
| **PayPal** | Payments | US |
| **Rare Areas** | Auto-bucket for other regions | (Collect nodes from “My Nodes” by negative regex that excludes HK/US/JP/KR/TW/SG) |

---

## 🧱 Rule Sources & Credits

- Base: Rabbit‑Spec Surge general skeleton  
- Rules: BlackMatrix7 · Surge (YouTube / Netflix / Disney / HBO / Hulu / Prime / Paramount+ / GlobalMedia / China / Google / Apple / Microsoft / Telegram / Twitter / TikTok / GitHub / PayPal, etc.)  
- Icons: Koolson/Qure IconSet · Orz‑3/mini Color

> If your node names do not contain region keywords or flags, please modify the `policy-regex-filter` in the config accordingly.

---

## 🙌 Contributing

**Feel free to use this or open issues.**

## 🛫 My Providers

- [**Flower**: very well-known; usually the first choice for streaming users. ~~(Can’t afford TAG, jk)~~](https://api-flowercloud.com/aff.php?aff=13383)
- [**YToo**: a sub-site of Flower, same features with slightly lower cost. Includes an Emby that I don’t find very useful.](https://y-too.com/aff.php?aff=7148)
- [**SNTP**: cost‑effective dedicated lines at mid/high tier (bundled high‑quality Emby server).](https://d.xn--hwqp2zit2amna.net/auth/register?code=BcADJolY)
