# ♟️ Deep Dive Python Chess Engine + Bot

Build a complete, FIDE-legal chess engine and bot in Python from scratch — no external libraries for game logic. This project is a full educational and engineering deep dive into chess programming and AI.

---

## 🚀 Project Overview

Implementation:
- A full chess rules engine (pieces, board, moves, special rules)
- Terminal-based gameplay
- A custom-built chess bot using Minimax + Alpha-Beta pruning
- An optional GUI (Pygame, Tkinter, etc.)
- Clean architecture, full test coverage, and deep rule enforcement

---

## 🛠️ Tech Stack

- Language: **Python**
- Interface: **Terminal (CLI)** → Optional: GUI (Pygame/Tkinter)
- Libraries: None for logic (built from scratch), optional for UI
- Bot: Custom **Minimax** with **alpha-beta pruning**

---

## 📋 Roadmap

### ✅ PHASE 1 — Board Representation & Core Structures
- [x] Define board structure (`8x8` or 1D list of 64 squares)
- [x] Create enums/constants for pieces and colors
- [x] Implement `Piece` class with type, color, has_moved
- [x] Implement `Move` class to represent all move metadata
- [x] Initialize and print the starting board

---

### ♟️ PHASE 2 — Piece Movement & Move Generation
- [x] Implement movement rules for:
  - [x] Pawn (incl. captures, double push)
  - [x] Knight
  - [x] Bishop
  - [x] Rook
  - [x] Queen
  - [x] King (incl. castling)
- [x] Generate pseudo-legal moves
- [x] Implement legal move filtering:
  - [x] King safety
  - [x] Pinned pieces
  - [x] Discovered checks

---

### ⚖️ PHASE 3 — Rule Enforcement
- [x] En passant (timing, legality)
- [x] Castling (rook/king unmoved, check rules)
- [x] Pawn promotion (default to queen, later user choice)
- [x] Threefold repetition detection
- [x] 50-move rule
- [x] Check/checkmate/stalemate detection

---

### 🎮 PHASE 4 — Game Management & CLI
- [x] Turn system
- [x] Input parsing (e.g., `e2e4`)
- [x] Output clean board state
- [x] Move validation
- [x] Undo/redo move stack
- [x] Move history
- [x] Save/load games (optional PGN format)

---

### 🧠 PHASE 5 — Evaluation Function
- [x] Material score
- [x] Piece-square tables
- [x] Pawn structure (doubled, isolated, passed)
- [x] King safety
- [x] Mobility
- [x] Normalize score per side to move

---

### 🤖 PHASE 6 — Bot Logic
- [x] Implement Minimax search (recursive)
- [x] Add Alpha-Beta pruning
- [x] Add iterative deepening
- [x] Add quiescence search
- [x] Add move ordering (captures first, killer moves)
- [x] Time-based or depth-based limits

---

### ⚙️ PHASE 7 — Optimization & Testing
- [x] Modularize code (board, game, logic, bot)
- [x] Profile for performance bottlenecks
- [x] Add unit tests for:
  - [x] Movement rules
  - [x] Special cases
  - [x] Game result detection
- [x] Add logging/debug mode
- [x] Document functions and architecture
- [x] Add type hints

---

### 🎨 PHASE 8 — Optional GUI
- [ ] Choose GUI library: Pygame / Tkinter / PyQt
- [ ] Render board and pieces
- [ ] Handle drag-and-drop or click input
- [ ] Show check/mate/stalemate
- [ ] Play against bot in GUI

---

### 🧠 Core Concepts to Learn Along the Way
- Bitboards vs arrays (you'll use arrays here)
- Chess engine search trees
- Alpha-beta pruning
- Evaluation heuristics
- Game state management
- Clean architecture and separation of concerns

---

## 📅 Project Timeline (Flexible Estimate)

| Phase         | Estimated Duration |
|---------------|--------------------|
| Phases 1–2    | 1–2 weeks          |
| Phases 3–4    | 1 week             |
| Phases 5–6    | 2–3 weeks          |
| Phase 7       | 1 week             |
| Phase 8 (GUI) | 1–2 weeks          |

--- 

### 📦 Folder Structure (Planned)

<details>
  <summary>📁 chess_engine</summary>

  <details>
    <summary>📁 core</summary>
    <ul>
      <li>📄 board.py</li>
      <li>📄 export.py</li>
      <li>📄 game_state.py</li>
      <li>📄 move.py</li>
      <li>📄 pgn.py</li>
      <li>📄 piece.py</li>
    </ul>
  </details>

  <details>
    <summary>📁 engine</summary>
    <ul>
      <li>📄 bot.py</li>
      <li>📄 evaluation.py</li>
      <li>📄 search.py</li>
    </ul>
  </details>

  <details>
    <summary>📁 tests</summary>
    <ul>
      <li>📄 test_pieces.py</li>
      <li>📄 test_rules.py</li>
      <li>📄 test_bot.py</li>
    </ul>
  </details>

  <details>
    <summary>📁 ui</summary>
    <ul>
      <li>📄 cli.py</li>
      <li>📄 gui.py</li>
    </ul>
  </details>

  <ul>
    <li>📄 main.py</li>
    <li>📄 README.md</li>
  </ul>

</details>

---

## 🧮 Evaluation Formula (Example)

```python
def evaluate(board):
    return (
        material_score(board) +
        position_bonus(board) +
        king_safety(board) +
        mobility_score(board)
    )
