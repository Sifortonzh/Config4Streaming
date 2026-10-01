# Atrioly · ShengXi — Geometry of Flowing Voices  

> *ShengXi* is the streaming configuration project under the **Atrioly / 序栖 (XuQi)** brand,  
> focusing on the intelligent segmentation of global media traffic, rule refinement,  
> and the aesthetic of network routing.  
>
> For the **Chinese version**, please refer to [README-zh.md](./README-zh.md)  
>
> **Loon version** available at → https://github.com/Sifortonzh/Loon4Streaming

---

# Key Features

## Local MESL / SNTP sync

Double-click [`tools/sync.command`](./tools/sync.command) to preview sanitized changes and validate them, then choose `1` to apply locally or `2` to apply and publish through SSH. Initialize once with `python3 tools/surge_sync.py --init`; initialization leaves the original profiles intact. See the [Chinese guide](./README-zh.md#本地-mesl--sntp-一键同步).

Shared settings live in [`templates/Surge.shared.conf`](./templates/Surge.shared.conf). Keep its `# @private:` markers. You can edit either iCloud profile or the template; changes since the previous sync are merged with Git three-way merging. Existing profile differences remain local. Conflicting changes stop before any files are overwritten. Subscription-containing lines and the complete `[Proxy]` block remain private, including any other options on those lines.

`python3 tools/surge_sync.py` previews only. Add `--apply --reload` to apply and reload the active Surge profile; add `--publish` to commit the designated public files and push `main`. `--source MESL` / `--source SNTP` selects the import source without overriding conflicts. Both public configurations, including the legacy `_0131` URL, are generated from the shared template with an example subscription URL.

Private fields come from each live profile. Baselines and private backups stay in Git-ignored `.surge-sync/`; never force-add this directory. Backups use `iCloud-` and `repo-` filename prefixes. To roll back, restore the corresponding files and that backup's `state.json`. Publication checks for current private values and refuses existing staged files or a branch behind remote `main`. A push failure leaves local changes and backups intact; retry after resolving SSH/network issues.

Requires Python 3, Git and Surge macOS. The default profile folder is the current user's iCloud Surge Documents folder; use `--icloud /your/path` when initializing a different folder. The baseline is bound to that folder. Concurrent sync processes are not supported. Run tests with `python3 -m unittest discover -s tools -p 'test_*.py'`.

- **Independent policy groups and priorities** for mainstream streaming platforms (YouTube / Netflix / Disney+ / Hulu / HBO Max / Prime Video / Paramount+ / Hayu / Bilibili, including Bstation).
- Regional groups (HK/US/JP/KR/TW/SG) + smart **Rare Areas** (automatically collects other unrecognized regions).
- Common service groups (Google, GitHub, Telegram, X, TikTok, PayPal, Apple, Microsoft, AI, etc.).
- Built on **Rabbit‑Spec [ShenXiangYouMiao]** general Surge skeleton + **BlackMatrix7** rule sets for Surge.
- Icons from **Koolson/Qure** and **Orz‑3/mini**.
- Default details: Google prefers HK, PayPal via US, Hayu via PH, Bilibili defaults to DIRECT.

> **Tip**: Replace `policy-path=YOUR_SUBSCRIPTION_URL` in the config with your own Surge subscription link (or the one provided by your provider).

---

# Directory Structure

## Repository Layout

```
Config4Streaming/
├─ Surge4Streaming.conf        
├─ rules/                       # list view
│  ├─ AI.list
│  ├─ ESPN.list
│  ├─ Google.list
│  ├─ HBOMax.list
│  ├─ Other_US.list
│  ├─ aol.list
│  ├─ proton.list
│  └─ yandex.list
├─ modules/                    # Surge JavaScript for ADBlock
│  ├─ baidupan_remove_ad.js
│  ├─ bilibili_player_ad.js
│  ├─ ...
├─ images/                     # Surge screenshots
│  ├─ Mac-1.png
│  ├─ Mac-2.png
│  └─ ...
├─ icons/                       YOUKU.png
├─ README.md
└─ README-zh.md
```

> All list files contain pure rule entries without policy fields and can be directly referenced using Surge RULE-SET.


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

# Quick Start (Surge · macOS)

1. Download [`Surge4Streaming.conf`](./Surge4Streaming.conf).  
2. In **Surge** → **Profiles** → **Open External Profile**, import the file. Or download from URL:

   ```bash
   https://raw.githubusercontent.com/Sifortonzh/Config4Streaming/refs/heads/main/Surge4Streaming.conf
   ```
3. Edit `policy-path=YOUR_SUBSCRIPTION_URL` to your real subscription URL.  
4. Save and enable.
5. On iOS, using “Modules” requires setting up the certificate; the method is the same as in Loon.

# Screenshots

## MacOS

![Surge Panel](./images/Mac.png)  

---

## iOS

![Surge Panel](./images/iOS.png)

---

# Policy Groups (Core)

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

# Rule Sources & Credits

- Base: Rabbit‑Spec Surge general skeleton  
- Rules: BlackMatrix7 · Surge (YouTube / Netflix / Disney / HBO / Hulu / Prime / Paramount+ / GlobalMedia / China / Google / Apple / Microsoft / Telegram / Twitter / TikTok / GitHub / PayPal, etc.)  
- Icons: Koolson/Qure IconSet · Orz‑3/mini Color

> If your node names do not contain region keywords or flags, please modify the `policy-regex-filter` in the config accordingly.

---

# Contributing

**Feel free to use this or open issues.**
