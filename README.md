# Chess Bot Project

### Disclaimer

This project was created purely for research, educational purposes, and for fun. The **Chess Bot** is designed to experiment with automation, machine learning, and chess engines like Stockfish.

**I do not endorse or encourage using this tool to cheat in any form of competitive or online chess games.** It is important to uphold the integrity of the game and respect the rules of any platform or competition you participate in. Misusing this bot to gain unfair advantages in chess games is against the spirit of this project.

**I am not responsible for any misuse of this software**. If you choose to use this tool in ways that violate the terms of service of chess platforms or in any unethical manner, that is solely your decision, and any consequences that arise are your responsibility.

Please use this project responsibly and enjoy chess the right way!

---

## Project Overview

This Chess Bot automates gameplay on a chess website by interacting with the web-based chessboard, using the **Stockfish** engine to compute moves. The project demonstrates the use of web automation, Python libraries for chess, and Stockfish integration to create a seamless chess-playing experience.

The bot performs the following key actions:
- Automates gameplay on a web-based chess platform.
- Uses **Stockfish**, one of the strongest open-source chess engines, to evaluate and select moves.
- Detects the current game state and reacts accordingly, including handling special cases such as pawn promotions and detecting game end conditions.
- Web scraping and automation through **Selenium** to interact with the webpage.

### Main Components

The project is organized into several modules, each handling specific aspects of the Chess Bot. Below is a breakdown of the core parts:

### 1. **`WebInterface`** (`src/bot/web_interface.py`)

This module handles all the interactions with the chess website. The **WebInterface** class provides methods to:
- **Navigate** the browser to the chess page.
- **Select computer level** and color for the game.
- **Generate pixel mapping** to map board squares to pixel coordinates.
- **Drag and drop pieces** on the board based on the Stockfish engine's moves.
- **Handle special moves** like pawn promotion by detecting the promotion interface and clicking the appropriate piece.

### 2. **`ChessEngine`** (`src/bot/chess_engine.py`)

This module is responsible for handling the chess logic and the interface with the **Stockfish** engine:
- **Translate chess moves** into a format usable by the web interface (UCI to board squares).
- **Get the best move** from the Stockfish engine based on the current board position.
- **Update the board** with the engine's moves to maintain synchronization between the web interface and the engine.
- **Detect game-ending conditions** like checkmate or stalemate.

### 3. **`ChessBot`** (`src/bot/chess_bot.py`)

This is the main class that ties everything together. The **ChessBot** class:
- **Plays the game** by coordinating between the web interface and the chess engine.
- **Keeps track of moves** by both the player and the computer, detecting new moves from the web interface and responding with the best moves calculated by Stockfish.
- **Handles endgame detection**, ensuring the game finishes cleanly when checkmate, stalemate, or timeout conditions are met.
- The main game loop resides here, where the bot detects the opponent's moves, computes responses, and sends them to the web interface to execute on the board.

### 4. **Utility Functions** (`src/utils/board_utils.py`)

This module contains utility functions that support the core functionality:
- **Mapping pieces to squares** on the board.
- **Detecting the last move** from the move table.
- Other helper functions to ensure smooth operation between the chess engine and the web interface.

### 5. **Testing** (`tests/`)

The `tests/` directory contains unit tests for the bot’s core functionality. Using **`unittest`** or **`pytest`**, you can test:
- **Board mappings** and piece detection.
- **Stockfish engine integration** and move generation.
- **Web interface interactions** like piece dragging and move detection.

### How to Run the Project

1. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
