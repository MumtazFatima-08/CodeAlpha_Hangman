# Mystery Word Challenge — 2.5D Hangman Game
**CodeAlpha Python Programming Internship — Task 1**

A desktop graphical Hangman game developed using standard **Python 3** and **Tkinter**. The application provides an engaging 2.5D paper-cut casual indie game aesthetic, full keyboard and mouse input handling, difficulty tiers, dynamic score calculation, mistake trackers, and a 3-tier hint assist system.

---

## 🎯 CodeAlpha Internship Task Scope

- Text/character-based Hangman game logic mapped to a modern GUI.
- Exactly 5 predefined tech words categorized into Easy, Medium, and Hard.
- Strict limit of 6 incorrect guesses before the game terminates.
- Demonstrates core Python concepts: `random`, collections (`dict`, `list`, `set`), string operations, branching, and object-oriented GUI structures.
- Standard-library-only implementation without third-party wheels or frameworks.

---

## ✨ Features

- **2.5D Paper-Cut Theme:** Light sky-blue palette, stacked push-buttons with tactile shadow edges, smooth cards, and celebratory confetti.
- **Dual Input System:** Click letters on the on-screen keyboard or use your physical computer keyboard.
- **Exact 5 Words Bank:**
  - **Easy:** `PYTHON`, `NETWORK`
  - **Medium:** `DATABASE`, `SECURITY`
  - **Hard:** `ALGORITHM`
- **3-Tier Hint System (X-Factor):**
  - **Hint 1 (FREE):** Contextual category clue.
  - **Hint 2 (-10 Pts):** Reveals the first letter.
  - **Hint 3 (-20 Pts):** Uncovers one unrevealed secret letter.
- **Live Statistics:** Tracks games played, victories, win rates, and highest session scores.

---

## 🕹 Game Rules & Scoring

| Action | Score Impact |
| :--- | :--- |
| **Starting Score** | `100 Points` |
| **Correct Guess** | `+10 Points` |
| **Incorrect Guess** | `-10 Points` & `+1 Mistake` |
| **Hint 1 (Category)** | `FREE (0 Points)` |
| **Hint 2 (First Letter)** | `-10 Points` |
| **Hint 3 (Reveal Letter)** | `-20 Points` |
| **Victory Bonus** | `+50 Points` |

*Score never drops below zero. The game ends in a win when all characters are uncovered or in a loss upon 6 mistakes.*

---

## 🚀 How to Run

### Requirements
- Python 3.8 or higher installed on your computer.

### Execution
1. Open your terminal or command prompt inside the project directory:
   ```bash
   python hangman.py