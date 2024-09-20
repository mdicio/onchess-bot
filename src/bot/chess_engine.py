import chess
from stockfish import Stockfish
import re
import random as rd


class ChessEngine:
    def __init__(self, stockfish_path, engine_depth=20, skill_level=20):
        self.engine_depth = engine_depth
        self.skill_level = skill_level
        self.stockfish_path = stockfish_path

    def setup_board(self):
        self.board = chess.Board()  # Initialize chess board

    def setup_engine(self):
        self.engine = Stockfish(self.stockfish_path)
        self.engine.set_depth(self.engine_depth)
        self.engine.set_skill_level(self.skill_level)

    def get_best_move(self):
        """
        Get the best move from the chess engine in UCI format.
        """

    def get_best_move(self, move_speed, deceive):
        """
        Get the best move from the chess engine in UCI format.
        """
        if move_speed == "normal":
            return self.engine.get_best_move()
        elif move_speed == "bullet":
            tc = rd.uniform(100, 1000)

            if deceive:
                # n = rd.uniform(2, 10)
                best_move = self.engine.get_best_move_time(tc)
                return best_move
            else:
                return self.engine.get_best_move_time(200)

        elif move_speed == "ultra_bullet":
            tc = rd.uniform(10, 20)

            if deceive:
                # n = rd.uniform(2, 10)
                best_move = self.engine.get_best_move_time(tc)
                return best_move
            else:
                return self.engine.get_best_move_time(50)

    def translate_move_to_web(self, move):
        """
        Translate a chess move to web-based interaction.

        Parameters:
        - move: The move to translate in UCI format (e.g., 'e2e4').

        Returns:
        - The start and end squares as tuples (e.g., ('e2', 'e4')).
        """
        start_square = move[:2]
        end_square = move[2:4]
        return start_square, end_square

    def update_board_with_move(self, move):
        """
        Push the given move to the chess board.

        Parameters:
        - move: The move to push in UCI or SAN format.
        """
        self.board.push_san(move)

    def set_fen_position(self):
        """
        Set the engine's FEN position based on the current board state.
        """
        self.engine.set_fen_position(self.board.fen())

    def get_evaluation(self):
        """
        Get the evaluation score for the current position.
        """
        return self.engine.get_evaluation()

    def is_game_over(self):
        """
        Checks if the game is over on the board.
        """
        return self.board.is_game_over()

    def is_checkmate(self):
        """
        Checks if the position is a checkmate.
        """
        return self.board.is_checkmate()

    def is_promotion(self, move_san):
        """
        Checks if the move is a pawn promotion.
        Promotion is indicated by a final 'n', 'b', 'q', or 'r', possibly followed by '+' or '#'.
        """
        # Check if the move is long enough to include a promotion
        if len(move_san) > 4:
            # Check second-to-last or last character for promotion piece
            return (
                move_san[-2] in "nbrq"
                if move_san[-1] in "+#"
                else move_san[-1] in "nbrq"
            )

        return False

    def quit(self):
        """
        Sends a quit command to the chess engine (if needed).
        """
        self.engine.send_quit_command()
