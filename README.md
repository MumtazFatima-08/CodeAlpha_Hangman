# 🎮 Mystery Word Challenge — Hangman

<p align="center">
  <strong>A polished 2.5D tech-themed Hangman game built for the CodeAlpha Python Programming Internship — Task 1.</strong>
</p>

<p align="center">
  <a href="https://mumtazfatima-08.github.io/CodeAlpha_Hangman/">
    <img src="https://img.shields.io/badge/🎮%20PLAY%20THE%20GAME-LIVE-success?style=for-the-badge" alt="Play the game" />
  </a>
</p>

> **🌐 Browser version:** Play instantly in your browser — no Python installation required.
>
> **🐍 Desktop version:** The original Python + Tkinter implementation is also preserved in this repository.

---

## ✨ What is it?

**Mystery Word Challenge** is a casual, tech-themed Hangman game with a playful **2.5D paper-cut visual style**. It combines classic Hangman mechanics with difficulty levels, a strategic hint system, scoring, mistake tracking, keyboard controls, and persistent game statistics.

The project was originally developed as a **Python/Tkinter desktop application** for the CodeAlpha internship and has now been extended with a **browser-playable HTML, CSS & JavaScript version**.

## 🚀 Play Online

### 👉 [🎮 PLAY MYSTERY WORD CHALLENGE](https://mumtazfatima-08.github.io/CodeAlpha_Hangman/)

Open the link and start playing instantly.

---

## 🎯 Features

- 🎨 **2.5D Paper-Cut UI** — bright sky-blue theme, tactile buttons, cards and playful visual elements.
- 🧠 **3 Difficulty Levels** — Easy, Medium and Hard.
- ⌨️ **Dual Input** — use the on-screen keyboard or your physical keyboard.
- 💡 **3-Tier Hint System** — choose between free clues and paid letter reveals.
- ❤️ **6-Mistake Rule** — the classic Hangman limit.
- 🏆 **Dynamic Scoring** — correct and incorrect guesses affect your score.
- 📊 **Persistent Statistics** — games, wins, win rate and best score are stored locally in the browser.
- 📱 **Responsive Design** — playable on desktop, tablet and mobile screens.
- ⚡ **No Backend Required** — the browser version runs entirely on the client side.

---

## 🧩 Word Bank

| Difficulty | Words |
|---|---|
| 🟢 Easy | `PYTHON`, `NETWORK` |
| 🟠 Medium | `DATABASE`, `SECURITY` |
| 🔴 Hard | `ALGORITHM` |

The game contains exactly **5 predefined technology-related words**, matching the original internship project.

---

## 💡 Hint System

| Hint | Cost | Effect |
|---|---:|---|
| 💡 Free Clue | `0` | Shows a contextual clue/fact about the word |
| 🔎 First Letter | `-10` | Reveals the first letter |
| ✨ Reveal Letter | `-20` | Reveals one unrevealed letter |

Hints are optional, so players can choose between playing strategically or using assistance.

---

## 🏆 Scoring System

| Action | Score |
|---|---:|
| Starting Score | `100` |
| Correct Guess | `+10` |
| Incorrect Guess | `-10` |
| Free Clue | `0` |
| First Letter Hint | `-10` |
| Reveal Letter Hint | `-20` |
| Victory Bonus | `+50` |

**Score cannot fall below zero.** A game is won when all letters are uncovered and lost after 6 incorrect guesses.

---

## 🛠️ Tech Stack

### Browser Version
- **HTML5** — structure
- **CSS3** — responsive 2.5D interface and animations
- **JavaScript** — game engine, keyboard controls, scoring, hints and local statistics
- **LocalStorage** — persistent player statistics and difficulty preference
- **GitHub Pages** — static deployment

### Original Desktop Version
- **Python 3**
- **Tkinter**
- Python Standard Library only

---

## 📁 Project Structure

```text
CodeAlpha_Hangman/
│
├── index.html          # Browser version
├── style.css           # Browser UI & responsive styling
├── script.js           # Browser game logic
├── hangman.py          # Original Python/Tkinter version
├── requirements.txt    # Python project requirements
├── run.bat             # Windows launcher for desktop version
├── PROJECT_NOTES.md    # Development notes
└── README.md           # Project documentation
```

---

## 🐍 Run the Original Python Version

### Requirements

- Python 3.8+
- Tkinter (normally included with standard Python installations)

### Run

```bash
python hangman.py
```

Or on Windows, run:

```text
run.bat
```

---

## 🌐 Browser Version

The web version was created specifically so the Hangman experience can be opened and played directly from a browser.

It does **not** replace the original Python/Tkinter project — both versions are preserved in the same repository.

### GitHub Pages

The intended deployment source is:

```text
Branch: main
Folder: / (root)
```

Once GitHub Pages is enabled, the game is available at:

**https://mumtazfatima-08.github.io/CodeAlpha_Hangman/**

---

## 📌 Internship Context

**Program:** CodeAlpha Python Programming Internship  
**Task:** Task 1 — Hangman Game  
**Original Language:** Python  
**Original GUI:** Tkinter  
**Web Extension:** HTML + CSS + JavaScript

---

## 👩‍💻 Author

**Mumtaz Fatima**  
CSE (AI & ML) Student | Aspiring AI Engineer

---

<p align="center">
  <strong>Made with Python first. Reimagined for the web. 🎮</strong>
</p>
