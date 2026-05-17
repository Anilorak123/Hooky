# 🧶 Yarnling — Cozy Crochet Idle Game

> Build your dream crochet business, one stitch at a time.

Yarnling is a cozy idle game for Android where you grow a handmade craft business from a humble ball of yarn into a thriving artisan empire. Craft scarves, plushies, and sweaters, sell them at markets, and unlock new patterns as your skills improve.

---

## 🎮 Gameplay

- **Craft** — produce handmade items using different yarn types and crochet patterns
- **Sell** — list your creations on a virtual marketplace and watch the coins roll in
- **Upgrade** — invest in better materials, tools, and workspace to boost production
- **Expand** — unlock new product categories, seasonal collections, and craft fairs
- **Idle** — progress continues even when you're away; come back to a full workshop

---

## ✨ Features

- Dozens of unlockable crochet patterns (amigurumi, blankets, accessories and more)
- Seasonal events with limited-edition items (Christmas, Easter, Valentine's Day)
- Cozy visual style with warm pastel colors
- Satisfying progression loop designed for short play sessions
- Offline earnings — your shop never closes
- Ad-supported with optional one-time purchase to remove ads

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Framework | Kivy / KivyMD |
| Target platform | Android (Google Play) |
| Ads | Google AdMob |
| Version control | Git / GitHub |

---

## 📁 Project Structure

```
yarnling/
├── main.py              # App entry point
├── screens/             # Individual game screens (main menu, workshop, shop…)
├── logic/               # Game mechanics (production, economy, upgrades)
├── assets/
│   ├── images/          # Sprites, backgrounds, UI elements
│   ├── fonts/           # Custom typefaces
│   └── sounds/          # SFX and background music
├── data/
│   └── items.json       # Item definitions, prices, unlock conditions
├── saves/               # Local save file handling
└── buildozer.spec       # Android build configuration
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Kivy 2.3+
- Buildozer (for Android builds)

### Run locally

```bash
git clone https://github.com/yourusername/yarnling.git
cd yarnling
pip install kivy
python main.py
```

### Build for Android

```bash
pip install buildozer
buildozer android debug
```

---

## 🗺️ Roadmap

- [x] Core idle loop (craft → sell → upgrade)
- [x] Save/load system
- [ ] First 20 unlockable patterns
- [ ] AdMob integration
- [ ] Seasonal events system
- [ ] Polish localization
- [ ] Google Play release
- [ ] Customer request system (special orders)
- [ ] Craft fair mini-events

---

## 🤝 Contributing

This is a solo indie project, but feedback and suggestions are very welcome! Feel free to open an issue if you spot a bug or have an idea for a new feature.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">Made with 🧶 and a lot of patience</p>
